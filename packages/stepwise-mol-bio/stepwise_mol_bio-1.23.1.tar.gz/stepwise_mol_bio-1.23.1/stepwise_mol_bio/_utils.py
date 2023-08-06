#!/usr/bin/env python3

import sys
import appcli
import autoprop
import tidyexc

from freezerbox import MakerConfig, iter_combo_makers
from appcli import Method, DocoptConfig
from appdirs import AppDirs
from inform import format_range, error
from more_itertools import all_equal
from functools import partial
from pathlib import Path

app_dirs = AppDirs("stepwise_mol_bio")

class Main(appcli.App):
    usage_io = sys.stderr
    group_by = {}
    merge_by = {}

    @classmethod
    def main(cls):
        app = cls.from_params()
        app.load(DocoptConfig)
        app.load(MakerConfig)
        
        try:
            app.protocol.print()
        except StepwiseMolBioError as err:
            error(err)

    @classmethod
    def make(cls, db, products, *, group_by=None, merge_by=None):
        if group_by is None:
            group_by = cls.group_by

        if merge_by is None:
            merge_by = cls.merge_by

        yield from iter_combo_makers(
                partial(cls._combo_maker_factory, db),
                map(cls._solo_maker_factory, products),
                group_by=group_by,
                merge_by=merge_by,
        )

    def refresh(self):
        autoprop.clear_cache(self)

    @classmethod
    def _solo_maker_factory(cls, product):
        app = cls.from_params()
        app.db = product.db
        app.products = [product]
        app.load(MakerConfig)
        return app

    @classmethod
    def _combo_maker_factory(cls, db):
        app = cls.from_params()
        app.db = db
        return app


class Cleanup(Main):

    product_tags = appcli.param(
            Method(lambda self: [x.tag for x in self.products]),
            default_factory=list,
    )

    def __bareinit__(self):
        super().__bareinit__()
        self.show_product_tags = False

    @classmethod
    def make(cls, db, products):
        makers = list(super().make(db, products))
        show_product_tags = (len(makers) != 1)

        for maker in makers:
            maker.show_product_tags = show_product_tags
            yield maker


@autoprop
class Argument(appcli.App):

    def __init__(self, tag, **kwargs):
        self.tag = tag
        self._set_known_attrs(kwargs)

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.tag!r})'

    def bind(self, app, force=False):
        if not hasattr(self, 'app') or force:
            self.app = app
            self.on_bind(app)

    def on_bind(self, app):
        pass

    def get_db(self):
        return self.app.db

    def _set_known_attrs(self, attrs):
        for attr, value in attrs.items():
            if attr not in self.__class__.__dict__:
                raise AttributeError(f"unknown attribute {attr!r}")
            setattr(self, attr, value)


class ShareConfigs:

    def on_bind(self, app):
        appcli.share_configs(app, self)



class StepwiseMolBioError(tidyexc.Error):
    pass

class ConfigError(StepwiseMolBioError):
    # For values that don't make sense, e.g. non-existent enzymes, etc.
    pass

class UsageError(StepwiseMolBioError):
    # For if the program isn't being used correctly, e.g. missing information.
    pass

def bind_arguments(app, reagents, iter=iter):
    for reagent in iter(reagents):
        reagent.bind(app)
    return reagents

def try_except(expr, exc, failure, success=None):
    try:
        x = expr()
    except exc:
        return failure()
    else:
        return success() if success else x

def hanging_indent(text, prefix):
    from textwrap import indent
    if not isinstance(text, str):
        text = '\n'.join(map(str, text))
    if isinstance(prefix, int):
        prefix = ' ' * prefix
    return indent(text, prefix)[len(prefix):]

def merge_dicts(dicts):
    result = {}
    for dict in reversed(list(dicts)):
        result.update(dict)
    return result

def comma_list(x):
    return [x.strip() for x in x.split(',')]

def comma_set(x):
    return {x.strip() for x in x.split(',')}

def int_or_expr(x):
    return type_or_expr(int, x)

def float_or_expr(x):
    return type_or_expr((float, int), x)

def type_or_expr(type, x):
    if isinstance(x, type):
        return x
    else:
        return type(eval(x))

def require_reagent(rxn, reagent):
    if reagent not in rxn:
        raise UsageError(f"reagent table missing {reagent!r}")

def merge_names(names):
    names = list(names)
    if all_equal(names):
        return names[0]
    else:
        return ','.join(names)

def match_len(x, n):
    # Something more generic than this might fit well in `more_itertools`.
    if isinstance(x, list):
        if len(x) != n:
            raise ValueError(f"expected {n} item(s), got {len(x)}")
        return x
    else:
        return n * [x]


def format_sec(x):
    if x < 60:
        return f'{x}s'

    min = x // 60
    sec = x % 60

    return f'{min}m{f"{sec:02}" if sec else ""}'

def format_min(x):
    if x < 60:
        return f'{x}m'

    hr = x // 60
    min = x % 60

    return f'{hr}h{f"{sec:02}" if min else ""}'

