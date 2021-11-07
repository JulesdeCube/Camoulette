import sys

from pathlib import Path

from camoulette.utils import _update_attibute


class Config:

    @staticmethod
    def __parse_load(load: None | str | list[str]) -> list[str]:
        if load is None:
            load = []
        elif isinstance(load, str):
            load = load.splitlines(False)
        # elif not isinstance(load, list):
        #    raise TypeError("wong type")

        return [line.strip() for line in load if load]

    def __init__(self,
                 path: Path,
                 *,
                 prelude: None | str = "",
                 load: None | str | list[str] = None,
                 extra_args: None | list[str] = None,
                 timeout: None | float | int = 1.0,
                 level: None | int = 0,
                 warning: None | bool = False) -> None:

        self._path: Path = path
        self._prelude: str = '' if prelude is None else prelude
        self._extra_args: list[str] = [] if extra_args is None else extra_args
        self._load: list[str] = self.__parse_load(load)
        self._timeout: float | None = 1.0 if timeout is None else float(timeout)
        self._level: int = 0 if level is None else level
        self._warning: bool = warning is not None and warning

    attributes = [
        'prelude', 'extra_args', 'timout', 'warning'
    ]

    def update(self, obj: object):
        for attribute in self.attributes:
            _update_attibute(self, obj, attribute)
        if hasattr(obj, 'load'):
            self._load += self.__parse_load(obj.load)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def warning(self) -> bool:
        return self._warning

    @property
    def prelude(self) -> str:
        return self._prelude

    @property
    def extra_args(self) -> list[str]:
        return self._extra_args

    @property
    def level(self) -> int:
        return self._level

    @property
    def timeout(self) -> float | None:
        return self._timeout

    @property
    def load(self) -> list[str]:
        # make it uneditable
        return list(self._load)

    @property
    def extra_args(self) -> list[str]:
        return self._extra_args

    @property
    def path(self) -> Path:
        return self._path

    @staticmethod
    def from_args() -> None:
        if len(sys.argv) != 2:
            print("usage: camoulette path")
            exit(1)
        return Config(Path(sys.argv[1]))
