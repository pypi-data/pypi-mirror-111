#!/usr/bin/env python3

import stepwise, appcli, autoprop, freezerbox
from math import sqrt, ceil
from numbers import Real
from inform import plural, indent
from appcli import Key, Method, DocoptConfig
from stepwise import (
        StepwiseConfig, PresetConfig, Quantity, UsageError,
        pl, ul, pre
)
from stepwise_mol_bio import (
        Main, Argument, ShareConfigs, ConfigError,
        comma_set, bind_arguments, require_reagent,
        int_or_expr, float_or_expr, merge_names,
)
from freezerbox import (
        ReagentConfig, MakerConfig, unanimous,
        parse_volume_uL, parse_temp_C, parse_time_s,
        group_by_identity, join_lists,
)
from more_itertools import first_true, flatten, chunked, all_equal, always_iterable
from statistics import mean
from collections.abc import Iterable
from copy import deepcopy
from operator import not_

# I'd like to support multiple <product> arguments, but first I need 
# MakerConfig to support multiple products (e.g. call unanimous, then fail 
# gracefully).

def find_amplicon(template, primer_1, primer_2, is_template_circular=False):
    from Bio.Seq import reverse_complement

    # This is a temporary solution until I implement full support for IDT-style 
    # sequence strings in freezerbox.
    template = freezerbox.normalize_seq(template)
    primer_1 = freezerbox.normalize_seq(primer_1)
    primer_2 = freezerbox.normalize_seq(primer_2)

    primer_pairs = [
            (primer_1, reverse_complement(primer_2)),
            (primer_2, reverse_complement(primer_1)),
    ]

    for fwd, rev in primer_pairs:
        # Assume perfect complementarity in the last 15 bases.  This isn't a 
        # good approach; better would be to predict where each oligo would 
        # anneal.  I think I could use Smith-Waterman for this.
        i = template.find(fwd[-15:  ])
        j = template.find(rev[   :15])

        if i < 0 or j < 0:
            continue

        if i < j:
            break

        if i > j:
            if is_template_circular:
                break
            else:
                continue

        if i == j:
            raise ValueError("primers bind same position")

    else:
        raise ValueError("no amplicon found")

    if i < j:
        return fwd[:-15] + template[i:j] + rev
    else:
        return fwd[:-15] + template[i:] + template[:j] + rev

def parse_amplicons_from_docopt(args):
    return [parse_amplicon(x) for x in args['<amplicons>']]

def parse_amplicons_from_freezerbox(fields):
    template = fields['template']
    fwd, rev = parse_primers(fields['primers'])
    return [Pcr.Amplicon.from_tags(template, fwd, rev)]

def parse_amplicon(string):
    fields = string.split(',')
    n = len(fields) if string else 0

    if n == 3:
        return Pcr.Amplicon.from_tags(*fields)

    err = ConfigError(string=string, n=n)
    err.brief = "can't interpret {string!r} as an amplicon"
    err.info += "expected 3 comma-separated fields (template, fwd, rev)"
    err.blame += "found {n}"
    raise err

def parse_primers(string):
    fields = string.split(',')
    n = len(fields) if string else 0

    if n == 2:
        return fields

    err = ConfigError(string=string, n=n)
    err.brief = "can't interpret {string!r} as a primer pair"
    err.info += "expected 2 comma-separated fields (fwd, rev)"
    err.blame += "found {n}"
    raise err

def temp(x):
    try:
        return float(x)
    except ValueError:
        return x

def time(x):
    return float(x)

@autoprop.cache
class Pcr(Main):
    """\
Amplify a DNA template using polymerase chain reaction (PCR).

Usage:
    pcr <amplicon>... [-a <°C>] [-x <sec> | -l <kb>] [options]
    pcr (-u <product>) [options]

Arguments:
    <amplicon>
        The names of the templates and forward/reverse primers to use for each 
        reaction, separated by commas.  If a `freezerbox` database is present 
        and these names can be found in it, default values for a number of 
        parameters (e.g. annealing temperate, extension time, etc.) will be 
        derived from it.

<%! from stepwise_mol_bio import hanging_indent %>\
Options:
    -p --preset <name>              [default: ${app.preset}]
        The default reaction and thermocycler parameters to use.  The following 
        sets of parameters are currently available:

        ${hanging_indent(app.preset_briefs, 8*' ')}

    -u --product <name>
        The name of a product to make.  This name must be present in the 
        FreezerBox database.  In this form of the command, all default settings 
        will be taken from the reaction used to synthesize the given product.

    -l --amplicon-length <bp>
        The length of the amplicon in base pairs (bp).  This can be used to 
        calculate an appropriate extension time.

    -n --num-reactions <int>        [default: ${app.num_reactions}]
        The number of reactions to set up.

    -v --reaction-volume <μL>
        The volume of the PCR reaction.

    -V --template-volume <µL>
        The volume of template to use in the reaction.  This overrides the 
        value specified by the preset.

    -T --template-stock <conc>
        The stock concentration of template to use in the reaction.  This 
        overrides the value specified by the preset, without affecting the 
        volume.  Include a unit, because none is implied.

    --primer-stock <µM>
        The stock concentration of the primers in µM.  Both primers must have 
        the same concentration.

    -y --num-cycles <n>
        The number of denature/anneal/extend cycles to perform, e.g. 35.

    --initial-denature-temp <°C>
        The temperature of the initial denaturation step in °C, e.g. 95.

    --initial-denature-time <sec>
        The duration of the initial denaturation step in seconds, e.g. 30.

    --denature-temp <°C>
        The temperature of the denaturation step in °C, e.g. 95.

    --denature-time <sec>
        The duration of the denaturation step in seconds, e.g. 10.

    -a --anneal-temp <°C>
        The temperature of the annealing step in °C, e.g. 60.  This is 
        determined by the sequence of the primers.
        
    -g --anneal-temp-gradient <range>
        The range of annealing temperatures that should be tried in a gradient 
        PCR reaction.  The range will be centered at the indicated annealing 
        temperature, and the protocol will indicate the corresponding high and 
        low temperatures.

    --anneal-time <sec>
        The duration of the annealing step in seconds, e.g. 20.

    --extend-temp <°C>
        The temperature of the extension step in °C, e.g. 72.
        
    -x --extend-time <sec>
        The duration of the extension step in seconds.  The rule of thumb is
        30 sec/kb, perhaps longer if you're amplifying a whole plasmid.

    --no-round-extend-time 
        When calculating an extension time from a given amplicon length (e.g. 
        `-l`), do *not* round the result to the nearest 30 sec increment.  Note 
        that when an explicit extension time is given (e.g. `-x`), it is never 
        rounded.

    --final-extend-temp <°C>
        The temperature of the final extension step in °C, e.g. 72.

    --final-extend-time <sec>
        The duration of the annealing step in seconds, e.g. 120.

    --hold-temp <°C>
        The temperature in °C to hold the reaction at after it completes.

    --melt-curve-low-temp <°C>
        The temperature in °C at which to begin recording a melt curve,
        e.g. 65.  This is only relevant for qPCR protocols.

    --melt-curve-high-temp <°C>
        The temperature in °C at which to stop recording a melt curve,
        e.g. 95.  This is only relevant for qPCR protocols.

    --melt-curve-temp-step <°C>
        How much to increment the temperature in °C at each step in the melt 
        curve, e.g. 0.5°C.  This is only relevant for qPCR protocols.

    --melt-curve-time-step <sec>
        The duration in seconds of each step in the melt curve, e.g. 5.  This 
        is only relevant for qPCR protocols.

    --two-step
        Specify that the annealing and extension steps should be combined, e.g. 
        if the primer melting temperatures are very close to the extension 
        temperature or if the amplicon is very short.

    --qpcr
        Specify that this is a qPCR protocol, i.e. that fluorescence should be 
        measured after each thermocyler cycle.
"""

    __config__ = [
            DocoptConfig.setup(usage_getter=lambda self: self.format_usage()),
            MakerConfig,
            PresetConfig,
            StepwiseConfig.setup('molbio.pcr'),
    ]
    usage = appcli.config_attr()
    preset_briefs = appcli.config_attr()

    @autoprop
    class Amplicon(ShareConfigs, Argument):
        __config__ = []

        def _calc_seq(self):
            try:
                return find_amplicon(
                        self.template.seq,
                        self.fwd.seq,
                        self.rev.seq,
                        self.template.is_circular,
                )
            except ValueError:
                err = ConfigError(
                        template=self.template,
                        fwd=self.fwd,
                        rev=self.rev,
                )
                err.brief = "{fwd.tag!r} and {rev.tag!r} do not amplify {template.tag!r}"
                err.info += "{template.tag}: {template.seq}"
                err.info += "{fwd.tag}: {fwd.seq}"
                err.info += "{rev.tag}: {rev.seq}"
                raise err from None

        seq = appcli.param(
                Method(_calc_seq),
        )
        length_bp = appcli.param(
                Key(DocoptConfig, '--amplicon-length', cast=float),
                Method(lambda self: len(self.seq)),
                default=None
        )

        @classmethod
        def from_tags(cls, template, fwd, rev, **kwargs):
            return cls(
                    Pcr.Template(template),
                    Pcr.Primer(fwd),
                    Pcr.Primer(rev),
                    **kwargs,
            )

        def __init__(self, template, fwd, rev, **kwargs):
            self.template = template
            self.fwd = fwd
            self.rev = rev
            self._set_known_attrs(kwargs)

        def __repr__(self):
            return f'{self.__class__.__qualname__}({self.template!r}, {self.fwd!r}, {self.rev!r})'

        def get_reagents(self):
            return self.template, *self.primers

        def get_reagent_tags(self):
            return tuple(x.tag for x in self.reagents)

        def get_primers(self):
            return self.fwd, self.rev

        def set_primers(self, primers):
            self.fwd, self.rev = primers

        def on_bind(self, app):
            super().on_bind(app)
            for reagent in self.reagents:
                reagent.bind(app)

    class Template(Argument):
        __config__ = [ReagentConfig]

        seq = appcli.param('seq')
        is_circular = appcli.param('is_circular')

    class Primer(ShareConfigs, Argument):
        __config__ = [ReagentConfig]

        seq = appcli.param(
                Key(ReagentConfig, 'seq'),
        )
        melting_temp_C = appcli.param(
                Key(ReagentConfig, 'melting_temp_C'),
        )
        stock_uM = appcli.param(
                Key(DocoptConfig, '--primer-stock', cast=float),
                Key(ReagentConfig, 'conc_uM'),
                Key(PresetConfig, 'primer_stock_uM'),
                Key(StepwiseConfig, 'primer_stock_uM'),
        )

    def _calc_anneal_temp_C(self):
        return [
                self.anneal_temp_func(
                    amplicon.fwd.melting_temp_C,
                    amplicon.rev.melting_temp_C,
                )
                for amplicon in self.amplicons
        ]

    def _calc_extend_time_s(self):
        bp = min(bp for x in self.amplicons if (bp := x.length_bp))

        def round(x):
            if not self.round_extend_time: return x
            if x <= 10: return 10
            if x <= 15: return 15
            return 30 * ceil(x / 30)

        if factor := self.extend_time_s_per_kb:
            return round(factor * bp / 1000)

        return round(self.extend_time_func(bp))

    presets = appcli.param(
            Key(StepwiseConfig, 'presets'),
            pick=list,
    )
    preset = appcli.param(
            Key(DocoptConfig, '--preset'),
            Key(MakerConfig, 'preset'),
            Key(StepwiseConfig, 'default_preset'),
    )
    amplicons = appcli.param(
            Key(DocoptConfig, parse_amplicons_from_docopt),
            Key(MakerConfig, parse_amplicons_from_freezerbox),
            get=bind_arguments,
    )
    product_tag = appcli.param(
            Key(DocoptConfig, '--product'),
    )
    products = appcli.param(
            Method(lambda self: [
                self.db[self.product_tag].make_intermediate(0)
            ]),
    )
    template_volume_uL = appcli.param(
            Key(DocoptConfig, '--template-volume', cast=float),
            default=None,
    )
    template_stock = appcli.param(
            Key(DocoptConfig, '--template-stock'),
            # Don't try to get a value from the amplicons/freezerbox database, 
            # because the template volume is not affected by this setting.
            default=None,
    )
    product_conc_ng_uL = appcli.param(
            Key(PresetConfig, 'product_conc_ng_uL'),
            default=50,
    )
    num_reactions = appcli.param(
            Key(DocoptConfig, '--num-reactions', cast=int_or_expr),
            Method(lambda self: len(self.amplicons)),
    )
    reaction_volume_uL = appcli.param(
            Key(DocoptConfig, '--reaction-volume'),
            Key(MakerConfig, 'volume', cast=parse_volume_uL),
            Key(PresetConfig, 'reaction_volume_uL'),
            cast=float_or_expr,
            default=None,
    )
    extra_volume_uL = appcli.param(
            Key(PresetConfig, 'extra_volume_uL'),
            Key(StepwiseConfig, 'extra_volume_uL'),
            cast=float_or_expr,
    )
    extra_percent = appcli.param(
            Key(PresetConfig, 'extra_percent'),
            Key(StepwiseConfig, 'extra_percent'),
            cast=float_or_expr,
    )
    base_reaction = appcli.param(
            Key(PresetConfig, 'reagents'),
            cast=stepwise.MasterMix.from_text,
    )
    num_cycles = appcli.param(
            Key(DocoptConfig, '--num-cycles'),
            Key(PresetConfig, 'num_cycles'),
            cast=int,
    )
    initial_denature_temp_C = appcli.param(
            Key(DocoptConfig, '--initial-denature-temp'),
            Key(PresetConfig, 'initial_denature_temp_C'),
            cast=temp,
    )
    initial_denature_time_s = appcli.param(
            Key(DocoptConfig, '--initial-denature-time'),
            Key(PresetConfig, 'initial_denature_time_s'),
            cast=time,
    )
    denature_temp_C = appcli.param(
            Key(DocoptConfig, '--denature-temp'),
            Key(PresetConfig, 'denature_temp_C'),
            cast=temp,
    )
    denature_time_s = appcli.param(
            Key(DocoptConfig, '--denature-time'),
            Key(PresetConfig, 'denature_time_s'),
            cast=time,
    )
    anneal_temp_C = appcli.param(
            Key(DocoptConfig, '--anneal-temp', cast=temp),
            Key(MakerConfig, 'Ta', cast=parse_temp_C),
            Method(_calc_anneal_temp_C),
            Key(PresetConfig, 'anneal_temp_C'),
    )
    anneal_temp_func = appcli.param(
            Key(PresetConfig, 'anneal_temp_func', cast=eval),
            default=lambda x: min(x) + 1,
    )
    anneal_temp_gradient_C = appcli.param(
            Key(DocoptConfig, '--anneal-temp-gradient'),
            Key(PresetConfig, 'anneal_temp_gradient_C'),
            cast=float,
    )
    anneal_time_s = appcli.param(
            Key(DocoptConfig, '--anneal-time'),
            Key(PresetConfig, 'anneal_time_s'),
            cast=time,
    )
    extend_temp_C = appcli.param(
            Key(DocoptConfig, '--extend-temp'),
            Key(PresetConfig, 'extend_temp_C'),
            cast=temp,
    )
    extend_time_s = appcli.param(
            Key(DocoptConfig, '--extend-time', cast=time),
            Key(MakerConfig, 'tx', cast=parse_time_s),
            Method(_calc_extend_time_s, skip=ValueError),
            Key(PresetConfig, 'extend_time_s'),
    )
    extend_time_s_per_kb = appcli.param(
            Key(PresetConfig, 'extend_time_s_per_kb'),
            cast=float,
    )
    extend_time_func = appcli.param(
            Key(PresetConfig, 'extend_time_func', cast=eval),
    )
    round_extend_time = appcli.param(
            Key(DocoptConfig, '--no-round-extend-time', cast=not_),
            Key(PresetConfig, 'round_extend_time'),
            Key(StepwiseConfig, 'round_extend_time'),
            default=True,
    )
    final_extend_temp_C = appcli.param(
            Key(DocoptConfig, '--final-extend-temp'),
            Key(PresetConfig, 'final_extend_temp_C'),
            cast=temp,
    )
    final_extend_time_s = appcli.param(
            Key(DocoptConfig, '--final-extend-time'),
            Key(PresetConfig, 'final_extend_time_s'),
            cast=time,
    )
    hold_temp_C = appcli.param(
            Key(DocoptConfig, '--hold-temp'),
            Key(PresetConfig, 'hold_temp_C'),
            cast=temp,
            default=None,
    )
    melt_curve_low_temp_C = appcli.param(
            Key(DocoptConfig, '--melt-curve-low-temp'),
            Key(PresetConfig, 'melt_curve_low_temp_C'),
            cast=temp,
    )
    melt_curve_high_temp_C = appcli.param(
            Key(DocoptConfig, '--melt-curve-high-temp'),
            Key(PresetConfig, 'melt_curve_high_temp_C'),
            cast=temp,
    )
    melt_curve_temp_step_C = appcli.param(
            Key(DocoptConfig, '--melt-curve-temp-step'),
            Key(PresetConfig, 'melt_curve_temp_step_C'),
            cast=temp,
    )
    melt_curve_time_step_s = appcli.param(
            Key(DocoptConfig, '--melt-curve-time-step'),
            Key(PresetConfig, 'melt_curve_time_step_s'),
            cast=temp,
    )
    two_step = appcli.param(
            Key(DocoptConfig, '--two-step'),
            Key(PresetConfig, 'two_step'),
            pick=first_true,
            default=False,
    )
    qpcr = appcli.param(
            Key(DocoptConfig, '--qpcr'),
            Key(PresetConfig, 'qpcr'),
            pick=first_true,
            default=False,
    )
    footnote = appcli.param(
            Key(PresetConfig, 'footnote'),
            default=None,
    )

    group_by = {
        'preset': group_by_identity,
        'reaction_volume_uL': group_by_identity,
    }
    merge_by = {
        'amplicons': join_lists,
        'anneal_temp_C': list,
        'extend_time_s': max,
    }

    @classmethod
    def from_product(cls, product_tag):
        self = cls.from_params()
        self.product_tag = product_tag
        self.load(MakerConfig)
        return self

    def __init__(self, amplicons):
        self.amplicons = amplicons

    def format_usage(self):
        return self.__doc__

    def get_protocol(self):
        protocol = stepwise.Protocol()
        pcr, primer_mix = self.reaction
        thermocycler = self.thermocycler_protocol
        footnotes = []

        # Primer mix (if applicable):

        example_uM = min(x.stock_uM for x in flatten(self.primer_pairs))
        footnotes.append(pl(
                f"For resuspending lyophilized primers:",
                f"{example_uM} µM = {1e3 / example_uM:g} µL/nmol",
                br='\n',
        ))

        if primer_mix:
            protocol += pl(
                    f"Prepare 10x primer mix{protocol.add_footnotes(*footnotes)}:",
                    primer_mix,
            )
            footnotes = []

        # PCR reaction setup:

        if self.footnote:
            # Before the footnote on resuspending the primers, if it hasn't 
            # been added to the protocol already.
            footnotes.insert(0, self.footnote)

        if x := pcr['template DNA'].stock_conc:
            footnotes.append(pl(
                    f"For diluting template DNA to {x}:",
                    f"Dilute 1 µL twice into {sqrt(1000/x.value):.1g}*sqrt([DNA]) µL",
                    br='\n',
            ))

        title = 'qPCR' if self.qpcr else 'PCR'
        instructions = ul()
        protocol += pl(
                f"Setup {plural(pcr.num_reactions):# {title} reaction/s}{protocol.add_footnotes(*footnotes)}:",
                pcr,
                instructions,
        )

        if pcr.volume > '50 µL':
            instructions += f"Split each reaction into {ceil(pcr.volume.value / 50)} tubes."
        if pcr.num_reactions > 1:
            instructions += "Use any extra master mix as a negative control."

        # Thermocycler protocol:

        protocol += pl(
                "Run the following thermocycler protocol:",
                thermocycler,
        )

        protocol.renumber_footnotes()
        return protocol

    def get_thermocycler_protocol(self):

        def temp(x):
            if isinstance(x, Iterable) and not isinstance(x, str):
                return merge_names(map(temp, x))
            elif isinstance(x, Real):
                return f'{x:g}°C'
            elif x[-1].isdigit():
                return f'{x}°C'
            else:
                return x

        def time(x):
            if isinstance(x, Iterable):
                return ','.join(map(temp, x))
            elif isinstance(x, str):
                return x
            elif x < 60:
                return f'{x:.0f}s'
            elif x % 60:
                return f'{x//60:.0f}m{x%60:02.0f}'
            else:
                return f'{x//60:.0f} min'

        def has_step(step, params=['temp_C', 'time_s']):
            return all(
                hasattr(self, f'{step}_{param}')
                for param in params
            )

        def step(step):
            if not hasattr(self, f'{step}_temp_gradient_C'):
                t = getattr(self, f'{step}_temp_C')
            else:
                t_mid = getattr(self, f'{step}_temp_C')
                t_mid = mean(always_iterable(t_mid))
                t_range = getattr(self, f'{step}_temp_gradient_C')
                t_low = round(t_mid - t_range / 2)
                t_high = round(t_low + t_range)
                t = f'{t_low}-{t_high}'

            return f"{temp(t)} for {time(getattr(self, f'{step}_time_s'))}"

        three_step = not self.two_step and has_step('extend')

        thermocycler_steps = [
                f"- {step('initial_denature')}",
                f"- Repeat {getattr(self, 'num_cycles')}x:",
                f"  - {step('denature')}",
                f"  - {step('anneal')}",
        ]
        if three_step:
            thermocycler_steps += [
                f"  - {step('extend')}",
            ]

        if self.qpcr:
            thermocycler_steps += [
                f"  - Measure fluorescence",
            ]

        if has_step('final_extend'):
            thermocycler_steps += [
                f"- {step('final_extend')}",
            ]

        if has_step('melt_curve', 'low_temp_C high_temp_C temp_step_C time_step_s'.split()):
            thermocycler_steps += [
                f"- {self.melt_curve_low_temp_C}-{self.melt_curve_high_temp_C}°C in {time(self.melt_curve_time_step_s)} steps of {self.melt_curve_temp_step_C}°C:",
            ]

        if self.qpcr:
            thermocycler_steps += [
                f"  - Measure fluorescence",
            ]

        if self.hold_temp_C:
            thermocycler_steps += [
                f"- {temp(self.hold_temp_C)} hold",
            ]

        return pre('\n'.join(thermocycler_steps))

    def get_reaction(self):
        pcr = deepcopy(self.base_reaction)
    
        require_reagent(pcr, 'water')
        require_reagent(pcr, 'template DNA')
        require_reagent(pcr, 'forward primer')
        require_reagent(pcr, 'reverse primer')

        pcr.extra_volume = self.extra_volume_uL, 'µL'
        pcr.extra_percent = self.extra_percent
        
        if self.num_reactions:
            pcr.num_reactions = self.num_reactions
        if self.reaction_volume_uL:
            pcr.hold_ratios.volume = self.reaction_volume_uL, 'µL'

        pcr['water'].order = 1

        pcr['template DNA'].order = 2
        pcr['template DNA'].name = merge_names(self.template_tags)
        pcr['template DNA'].master_mix = all_equal(self.template_tags)

        if x := self.template_volume_uL:
            pcr['template DNA'].volume = x, 'µL'
        if x := self.template_stock:
            pcr['template DNA'].stock_conc = x

        # Setup the primers.  This is complicated because the primers might 
        # get split into their own mix, if the volumes that would be added 
        # to the PCR reaction are too small.

        primer_mix = None
        primer_keys = [
                'forward primer',
                'reverse primer',
        ]
        use_primer_mix = []

        for p, primers in zip(primer_keys, zip(*self.primer_pairs)):
            pcr[p].order = 3
            pcr[p].name = merge_names(x.tag for x in primers)
            pcr[p].hold_conc.stock_conc = min(x.stock_uM for x in primers), 'µM'
            pcr[p].master_mix = all_equal(x.tag for x in primers)

            primer_scale = pcr.scale if pcr[p].master_mix else 1
            primer_vol = primer_scale * pcr[p].volume

            if primer_vol < '0.5 µL':
                use_primer_mix.append(p)

        if use_primer_mix:
            pcr['primer mix'].order = 4
            pcr['primer mix'].stock_conc = '10x'
            pcr['primer mix'].volume = pcr.volume / 10
            pcr['primer mix'].master_mix = all(
                    pcr[p].master_mix
                    for p in use_primer_mix
            )

            primer_mix = stepwise.MasterMix()
            primer_mix.volume = pcr.volume

            for p in use_primer_mix:
                primer_mix[p].name = pcr[p].name
                primer_mix[p].stock_conc = pcr[p].stock_conc
                primer_mix[p].volume = pcr[p].volume
                primer_mix[p].hold_stock_conc.conc *= 10
                del pcr[p]

            primer_mix.hold_ratios.volume = '10 µL'

        return pcr, primer_mix

    def get_templates(self):
        return [x.template for x in self.amplicons]

    def get_template_tags(self):
        return [x.tag for x in self.templates]

    def get_primer_pairs(self):
        return [(x.fwd, x.rev) for x in self.amplicons]

    def get_product_seqs(self):
        return [x.seq for x in self.amplicons]

    def get_product_conc(self):
        return Quantity(self.product_conc_ng_uL, 'ng/µL')

    def get_product_volume(self):
        pcr, primers = self.reaction
        return pcr.volume

    def get_product_molecule(self):
        return 'dsDNA'

    @property
    def is_product_circular(self):
        return False

    def get_dependencies(self):
        return set(flatten(x.reagent_tags for x in self.amplicons))

if __name__ == '__main__':
    Pcr.main()

