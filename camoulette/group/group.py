from inspect import isclass
from pathlib import Path
from camoulette.abc import AbcTest
from camoulette.file import File
from camoulette.group.group_result import GroupResult
from camoulette.utils import normalize_code
from typing import List, Dict


class Group(AbcTest):

    __tests: List[AbcTest]

    def __sub_tests(self, group_cls: type = AbcTest):

        def is_public(name: str):
            return not name.startswith('_') and name != 'parrent'

        def is_sub_class(cls: type):
            return isclass(cls) and issubclass(cls, group_cls)

        cls = self.__class__
        public_name = filter(is_public, list(self.__dict__) + list(cls.__dict__))
        public_class = map(self.__getattribute__, public_name)
        tests = filter(is_sub_class, public_class)
        return list(tests)

    def __init__(self, *, parent: AbcTest = None) -> None:
        super().__init__(parent=parent)
        if self.exercice:
            if not hasattr(self, "file"):
                raise Exception(
                    f"{self.name}: exercice need to define the 'file' attribute")

            if not self.file in self.load:
                self.load.append(self.file)

        self.__tests = [subtest(parent=self) for subtest in self.__sub_tests()]

    def __call__(self, path: Path, *,
                 files: Dict[str, File] = None) -> GroupResult:
        if files is None:
            files = {}
        return GroupResult(self,
                           [test(path, files=files) for test in self.__tests])

    @property
    def exercice(self):
        return hasattr(self, 'correction')
