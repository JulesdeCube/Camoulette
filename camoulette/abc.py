from __future__ import annotations

from abc import ABC

from inspect import isclass
from camoulette.utils import STRICT


def set_default(src: object, comp: dict):
    for key, value in comp.items():
        if not hasattr(src, key):
            src.__dict__[key] = value


def heredity(src: object, comp: object):
    for key in dir(comp):
        value = comp.__getattribute__(key)
        if not hasattr(src, key) and not (
                isclass(value) and issubclass(value, AbcTest)):
            src.__dict__[key] = value


class AbcTest(ABC):

    __default = {
        'warning': False,
        'extra_args': [],
        'timeout': 1.0,
        'prelude': '',
        'mode': STRICT
    }

    parent: None | AbcTest
    name: str
    coef: float

    warning: bool
    extra_args: list[str]

    load: list[str]
    prelude: str

    timeout: float
    mode: int

    def __init__(self, *, parent: AbcTest) -> None:

        correction = hasattr(self, 'correction')

        parrent_name = f"{parent.name}." if parent is not None else ''
        self.parent = parent
        # overwrite the name (no heredity)
        set_default(
            self, {'name': parrent_name + self.__class__.__name__,
                   'coef': 1.0,
                   'load': []})
        # heredity
        if parent is not None:
            heredity(self, parent)

            self.load += parent.load
        # set default
        set_default(self, AbcTest.__default)

        if not correction and hasattr(self, 'correction'):
            delattr(self, 'correction')

        super().__init__()
