import inspect
from difflib import SequenceMatcher

BIN = "/nix/store/6jsqrblnldrkwm8l0l10yrh29z9sb0g1-ocaml-4.12.0/bin/ocaml"


class MissingAttribute(Exception):
    def __init__(self, attribute: str) -> None:
        super().__init__(f"Missing class atribute: \"{attribute}\"")


def _check_attribute(obj: object, attibute: str) -> None:
    if not hasattr(obj, attibute):
        raise MissingAttribute(attibute)


def _set_default_attribute(obj: object, attribute: str, default: any):
    if not hasattr(obj, attribute):
        obj.__setattr__(attribute, default)


def _update_attibute(obj: object, src: object, name: str):
    if hasattr(src, name):
        obj.__setattr__('_' + name, _get_or_exec(src.__getattribute__(name)))


def _get_or_exec(value: any, *args, **kwargs) -> any:
    if inspect.ismethod(value) or inspect.isfunction(value):
        return value(*args, **kwargs)
    else:
        return value


def _get_ratio(string1: str, string2: str) -> float:
    return min(
        SequenceMatcher(None, string1, string2).ratio(),
        SequenceMatcher(None, string2, string1).ratio(),
    )
