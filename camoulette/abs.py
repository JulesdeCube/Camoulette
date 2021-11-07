from inspect import isclass
from camoulette.config import Config

from camoulette.utils import _set_default_attribute

class AbstractResult:
    pass

class AbstractTest:

    def __init__(self) -> None:
        _set_default_attribute(self, 'coef', 1)

    def run(self, config: Config) -> AbstractResult:
        config.update(self)

    @staticmethod
    def is_subclass(cls):
        return isclass(cls) and issubclass(cls, AbstractTest)

    @property
    def name(self) -> str:
        return self.__class__.__name__
