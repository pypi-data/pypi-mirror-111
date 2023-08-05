#!/usr/bin/env python3

import stepwise
import appcli
import autoprop
import re
import json
import requests

from stepwise_mol_bio import (
        Main, Argument, ShareConfigs, UsageError, ConfigError,
        bind_arguments, app_dirs, comma_list, match_len, int_or_expr,
)
from stepwise import StepwiseConfig, pl, ul
from freezerbox import (
        ReagentConfig, MakerConfig,
        parse_mass_ug, parse_volume_uL, parse_size_bp, parse_time,
        group_by_identity, join_lists,
)
from appcli import Key, Method, DocoptConfig
from inform import Error, plural, did_you_mean
from functools import partial
from pathlib import Path

def parse_templates_from_csv(string):
    return [
            RestrictionDigest.Template(x)
            for x in comma_list(string)
    ]

def parse_template_from_freezerbox(string):
    return [RestrictionDigest.Template(string)]

def pick_compatible_buffer(enzymes):
    if len(enzymes) == 1:
        return enzymes[0]['recommBuffer']

    # Don't consider `buf5`.  This is the code for buffers that are unique to a 
    # specific enzyme, so even if two enzymes both want `buf5`, it's not the 
    # same buffer.

    buffer_names = {
            '1': "NEBuffer r1.1",
            '2': "NEBuffer r2.1",
            '3': "NEBuffer r3.1",
            '4': "rCutSmart Buffer",
    }
    buffer_scores = {
            k: (
                sum(not x[f'star{k}'] for x in enzymes),  # Star activity?
                sum(x[f'buf{k}'] for x in enzymes),       # Cutting activity?
                k == '4',                                 # Prefer CutSmart
            )
            for k in buffer_names
    }
    best_buffer = max(
            buffer_scores,
            key=lambda k: buffer_scores[k],
    )

    return buffer_names[best_buffer]

def calc_digest_products(seq, enzymes, *, is_circular):
    from more_itertools import pairwise, flatten
    from Bio.Restriction import RestrictionBatch
    from Bio.Seq import Seq

    if not enzymes:
        raise UsageError("no enzymes specified", enzymes=enzymes)

    enzymes = [
            re.sub('-HF(v2)?$', '', x)
            for x in enzymes
    ]

    try:
        batch = RestrictionBatch(enzymes)
    except ValueError:
        raise ConfigError(
                lambda e: f"unknown enzyme(s): {','.join(map(repr, e.enzymes))}",
                enzymes=enzymes,
        ) from None

    sites = [x-1 for x in flatten(batch.search(Seq(seq)).values())]

    if not sites:
        raise ConfigError(
                lambda e: f"{','.join(map(repr, e.enzymes))} {plural(enzymes):/does/do} not cut template.",
                enzymes=enzymes,
                seq=seq,
        )

    sites += [] if is_circular else [0, len(seq)]
    sites = sorted(sites)

    seqs = []
    for i,j in pairwise(sorted(sites)):
        seqs.append(seq[i:j])

    if is_circular:
        wrap_around = seq[sites[-1]:] + seq[:sites[0]]
        seqs.append(wrap_around)

    return seqs

def calc_digest_product(seq, enzymes, *, is_circular, target_size=None):
    target_size = target_size or len(seq)
    product_seqs = calc_digest_products(seq, enzymes, is_circular=is_circular)
    return min(product_seqs, key=lambda x: abs(target_size - len(x)))

@autoprop.cache
class RestrictionDigest(Main):
    """\
Perform restriction digests using the protocol recommended by NEB.

Usage:
    digest <templates> <enzymes> [-d <ng>] [-D <ng/µL>] [-v <µL>] [-n <rxns>]
        [-g]
    digest <product> [-e <enzymes>] [options]

Arguments:
    <templates>
        The DNA to digest.  Use commas to specify multiple templates.  The 
        number of reactions will equal the number of templates.

    <enzymes>
        The restriction enzymes to use.  Only NEB enzymes are currently 
        supported.  If you are using an "HF" enzyme, specify that explicitly.  
        For example, "HindIII" and "HindIII-HF" have different protocols.  
        Enzyme names are case-insensitive, and multiple enzymes can be 
        specified using commas.

    <product>
        A product in the FreezerBox database that was synthesized by 
        restriction digest.  If this form of the command is given, the protocol 
        will take all default values (including the template and enzymes) from 
        the reaction used to synthesize the given product.

Options:
    -d --dna <µg>               [default: ${app.dna_ug}]
        The amount of DNA to digest, in µg.

    -D --dna-stock <ng/µL>
        The stock concentration of the DNA template, in ng/µL.

    -v --target-volume <µL>     [default: ${app.target_volume_uL}]
        The ideal volume for the digestion reaction.  Note that the actual 
        reaction volume may be increased to ensure that the volume of enzyme 
        (which is determined by the amount of DNA to digest, see --dna) is less 
        than 10% of the total reaction volume, as recommended by NEB.

    -t --time <min>
        Incubate the digestion reaction for a non-standard amount of time.  You 
        may optionally specify a unit.  If you don't, minutes are assumed.

    -n --num-reactions <int>
        The number of reactions to setup.  By default, this is inferred from 
        the number of templates.

    -g --genomic
        Indicate that genomic DNA is being digested.  This will double the 
        amount of enzyme used, as recommended by NEB.

    -e --enzymes <list>
        The same as <enzymes>, but for when a product is specified.  
    """
    __config__ = [
            DocoptConfig,
            MakerConfig,
            StepwiseConfig.setup('molbio.digest'),
    ]

    class Template(ShareConfigs, Argument):
        __config__ = [ReagentConfig]

        seq = appcli.param(
                Key(ReagentConfig, 'seq'),
        )
        stock_ng_uL = appcli.param(
                Key(DocoptConfig, '--dna-stock'),
                Key(ReagentConfig, 'conc_ng_uL'),
                Key(StepwiseConfig, 'dna_stock_ng_uL'),
                cast=float,
        )
        is_circular = appcli.param(
                Key(ReagentConfig, 'is_circular'),
                default=True,
        )
        is_genomic = appcli.param(
                Key(DocoptConfig, '--genomic'),
                default=False,
        )
        target_size_bp = appcli.param(
                Key(MakerConfig, 'size', cast=parse_size_bp),
                default=None,
        )

    templates = appcli.param(
            Key(DocoptConfig, '<templates>', cast=parse_templates_from_csv),
            Key(MakerConfig, 'template', cast=parse_template_from_freezerbox),
            get=bind_arguments,
    )
    enzyme_names = appcli.param(
            Key(DocoptConfig, '<enzymes>', cast=comma_list),
            Key(DocoptConfig, '--enzymes', cast=comma_list),
            Key(MakerConfig, 'enzymes', cast=comma_list),
    )
    product_tag = appcli.param(
            Key(DocoptConfig, '<product>'),
    )
    products = appcli.param(
            Method(lambda self: [
                self.db[self.product_tag].make_intermediate(0)
            ]),
    )
    num_reactions = appcli.param(
            Key(DocoptConfig, '--num-reactions', cast=int_or_expr),
            Method(lambda self: len(self.templates)),
    )
    dna_ug = appcli.param(
            Key(DocoptConfig, '--dna', cast=partial(parse_mass_ug, default_unit='µg')),
            Key(MakerConfig, 'mass', cast=parse_mass_ug),
            Key(StepwiseConfig),
            cast=float,
            default=1,
    )
    target_volume_uL = appcli.param(
            Key(DocoptConfig, '--target-volume', cast=partial(parse_volume_uL, default_unit='µL')),
            Key(MakerConfig, 'volume', cast=parse_volume_uL),
            Key(StepwiseConfig),
            default=10,
    )
    target_size_bp = appcli.param(
            Key(MakerConfig, 'size', cast=parse_size_bp),
            default=None,
    )
    time = appcli.param(
            Key(DocoptConfig, '--time', cast=partial(parse_time, default_unit='min')),
            Key(MakerConfig, 'time', cast=parse_time),
            default=None,
    )

    group_by = {
        'enzyme_names': group_by_identity,
        'dna_ug': group_by_identity,
        'target_volume_uL': group_by_identity,
        'time': group_by_identity,
    }
    merge_by = {
        'templates': join_lists,
    }

    @classmethod
    def from_tags(cls, template_tags, enzyme_names, db=None):
        templates = [cls.Template(x) for x in template_tags]
        return cls(templates, enzyme_names, db)

    @classmethod
    def from_product(cls, product_tag):
        self = cls.from_params()
        self.product_tag = product_tag
        self.load(MakerConfig)
        return self


    def __bareinit__(self):
        self._enzyme_db = None

    def __init__(self, templates, enzyme_names, db=None):
        self.templates = templates
        self.enzyme_names = enzyme_names
        self.enzyme_db = db

    def get_enzymes(self):
        return [self.enzyme_db[x] for x in self.enzyme_names]

    def get_enzyme_db(self):
        if self._enzyme_db is None:
            self._enzyme_db = NebRestrictionEnzymeDatabase()
        return self._enzyme_db

    def set_enzyme_db(self, db):
        self._enzyme_db = db

    def get_reaction(self):
        # Define a prototypical restriction digest reaction.  Stock 
        # concentrations for BSA, SAM, and ATP come from the given catalog 
        # numbers.

        rxn = stepwise.MasterMix.from_text("""\
        Reagent   Catalog      Stock    Volume  MM?
        ========  =======  =========  ========  ===
        water                         to 50 µL  yes
        DNA                200 ng/µL      5 µL  yes
        buffer                   10x      5 µL  yes
        bsa         B9200   20 mg/mL      0 µL  yes
        sam         B9003      32 mM      0 µL  yes
        atp         P0756      10 mM      0 µL  yes
        """)

        # Plug in the parameters the user requested.

        rxn.num_reactions = self.num_reactions

        rxn['DNA'].name = ','.join(x.tag for x in self.templates)
        rxn['DNA'].hold_conc.stock_conc = min(
                x.stock_ng_uL for x in self.templates), 'ng/µL'

        if len(self.templates) > 1:
            rxn['DNA'].order = -1
            rxn['DNA'].master_mix = False
        
        for enz in self.enzymes:
            key = enz['name']
            stock = enz['concentration'] / 1000
            is_genomic = any(x.is_genomic for x in self.templates)

            # The prototype reaction has 1 µg of DNA.  NEB recommends 10 U/µg 
            # (20 U/µg for genomic DNA), so set the initial enzyme volume 
            # according to that.  This will be adjusted later on.

            rxn[key].stock_conc = stock, 'U/µL'
            rxn[key].volume = (20 if is_genomic else 10) / stock, 'µL'
            rxn[key].master_mix = True

        rxn['buffer'].name = pick_compatible_buffer(self.enzymes)

        # Supplements

        known_supplements = []

        def add_supplement(key, name, unit, scale=1):
            conc = max(x['supplement'][key] for x in self.enzymes)
            known_supplements.append(key)

            if not conc:
                del rxn[key]
            else:
                rxn[key].hold_stock_conc.conc = conc * scale, unit
                rxn[key].name = name

        add_supplement('bsa', 'rAlbumin', 'mg/mL', 1e-3)
        add_supplement('sam', 'SAM', 'mM', 1e-3)
        add_supplement('atp', 'ATP', 'mM')

        # Make sure there aren't any supplements we should add that we don't 
        # know about.
        
        for enzyme in self.enzymes:
            for supp, conc in enzyme['supplement'].items():
                if conc > 0 and supp not in known_supplements:
                    err = ConfigError(
                            enzyme=enzyme,
                            supp=supp,
                            conc=conc,
                    )
                    err.brief = "{enzyme[name]!r} requires an unknown supplement: {supp!r}"
                    err.hints += "the restriction digest protocol needs updated"
                    err.hints += "please submit a bug report"
                    raise err
        
        # Update the reaction volume.  This takes some care, because the 
        # reaction volume depends on the enzyme volume, which in turn depends 
        # on the DNA quantity.

        k = self.dna_ug / 1  # The prototype reaction has 1 µg DNA.
        dna_vol = k * rxn['DNA'].volume
        enz_vols = {
                enz['name']: k * rxn[enz['name']].volume
                for enz in self.enzymes
        }
        enz_vol = sum(enz_vols.values())

        rxn.hold_ratios.volume = max(
                stepwise.Quantity(self.target_volume_uL, 'µL'),
                10 * enz_vol,

                # This is a bit of a hack.  The goal is to keep the water 
                # volume non-negative, but it won't necessarily work if there 
                # are supplements.
                10/9 * (dna_vol + enz_vol),
        )

        rxn['DNA'].volume = dna_vol
        for enz in self.enzymes:
            key = enz['name']
            rxn[key].volume = enz_vols[key]

        return rxn

    def del_reaction(self):
        pass

    def get_protocol(self):
        from itertools import groupby
        from operator import itemgetter

        protocol = stepwise.Protocol()
        rxn = self.reaction
        rxn_type = (
                self.enzymes[0]['name']
                if len(self.enzymes) == 1 else
                'restriction'
        )

        def incubate(temp_getter, time_getter, time_formatter=lambda x: f'{x} min'):
            incubate_params = [
                    (k, max(time_getter(x) for x in group))
                    for k, group in groupby(self.enzymes, temp_getter)
            ]
            return [
                    f"{temp}°C for {time_formatter(time)}"
                    for temp, time in sorted(incubate_params)
            ]

        if self.time:
            digest_steps = incubate(
                    itemgetter('incubateTemp'),
                    lambda x: self.time,
                    lambda x: x,
            )
        else:
            digest_steps = incubate(
                    itemgetter('incubateTemp'),
                    lambda x: 15 if x['timeSaver'] else 60,
                    lambda x: '5–15 min' if x == 15 else '1 hour',
            )

        inactivate_steps = incubate(
                itemgetter('heatInactivationTemp'),
                itemgetter('heatInactivationTime'),
        )

        protocol += pl(
            f"Setup {plural(rxn.num_reactions):# {rxn_type} digestion/s} [1,2]:",
            rxn,
        )
        protocol += pl(
            f"Incubate at the following temperatures [3]:",
            ul(*digest_steps, *inactivate_steps),
        )

        urls = [x['url'] for x in self.enzymes if x.get('url')]
        protocol.footnotes[1] = pl(*urls, br='\n')
        protocol.footnotes[2] = """\
NEB recommends 5–10 units of enzyme per µg DNA 
(10–20 units for genomic DNA).  Enzyme volume 
should not exceed 10% of the total reaction 
volume to prevent star activity due to excess 
glycerol.
"""
        protocol.footnotes[3] = """\
The heat inactivation step is not necessary if 
the DNA will be purified before use.
"""
        return protocol

    def del_protocol(self):
        pass

    def get_dependencies(self):
        return {x.tag for x in self.templates}

    def get_product_seqs(self):
        for template in self.templates:
            with ConfigError.add_info("tag: {tag}", tag=template.tag):
                yield calc_digest_product(
                        seq=template.seq,
                        enzymes=self.enzyme_names,
                        target_size=template.target_size_bp,
                        is_circular=template.is_circular,
                )

    def get_product_conc(self):
        return self.reaction['DNA'].conc

    def get_product_volume(self):
        return self.reaction.volume


class NebRestrictionEnzymeDatabase:

    def __init__(self, cache_path=None):
        self.cache_path = cache_path or Path(app_dirs.user_cache_dir) / 'neb' / 'restriction_enzymes.json'
        self.load_cache()

    def __getitem__(self, name):
        try:
            return self.enzyme_params[name.lower()]

        except KeyError:
            try:
                self.download_cache()
                self.load_cache()
                return self.enzyme_params[name.lower()]

            except (KeyError, ConfigError) as err1:
                err2 = ConfigError(
                        enzyme=name,
                        known_enzymes=self.enzyme_names,
                        fresh_download=not isinstance(err1, ConfigError),
                )
                err2.brief = "no such enzyme {enzyme!r}"
                err2.info += lambda e: (
                        f"successfully downloaded the most recent restriction enzyme data from NEB (in case {e.enzyme!r} is a new enzyme)"
                        if e.fresh_download else
                        f"failed to download the most recent restriction enzyme data from NEB (in case {e.enzyme!r} is a new enzyme)"
                )
                err2.hints += lambda e: f"did you mean: {did_you_mean(e.enzyme, e.known_enzymes)!r}"

                raise err2 from err1

    def load_cache(self):
        if not self.cache_path.exists():
            self.download_cache()

        with self.cache_path.open() as f:
            data = json.load(f)

        self.enzyme_names = list(data.keys())
        self.enzyme_params = {k.lower(): v for k, v in data.items()}

    def download_cache(self):
        url = 'http://nebcloner.neb.com/data/reprop.json'

        try:
            data = requests.get(url).json()

        except requests.exceptions.ConnectionError as err1:
            err2 = ConfigError(url=url)
            err2.brief = "failed to download restriction enzyme data from NEB"
            err2.info += "URL: {url}"
            err2.hints += "make sure the internet is connected and the above URL is reachable."
            raise err2 from err1

        else:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)

            with self.cache_path.open('w') as f:
                json.dump(data, f)

if __name__ == '__main__':
    RestrictionDigest.main()
