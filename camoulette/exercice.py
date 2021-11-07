from .groupe import Groupe
from .config import Config
from .test import Test


class Exercice(Groupe):
    def run(self, config: Config):
        for test in self._get_sub_test(Test):
            print(test)
            result = test().run(config)
            print(result)
