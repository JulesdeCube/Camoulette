from camoulette.runner import Result
from .abs import AbstractTest
from .config import Config


class GroupeResult:

    name: str


class Groupe(AbstractTest):

    def _get_sub_test(self, group_cls: type):

        def is_public(name: str):
            return not name.startswith('_')

        cls = self.__class__
        public_name = filter(is_public, cls.__dict__)
        public_class = map(self.__getattribute__, public_name)
        tests = filter(group_cls.is_subclass, public_class)
        return list(tests)

    def run(self, config: Config):

        def run_test(test) -> Result:
            test().run(config)

        config.update(self)
        tests = self._get_sub_test(AbstractTest)
        result = list(map(run_test, tests))
        return GroupeResult(self.name, self.na, result)