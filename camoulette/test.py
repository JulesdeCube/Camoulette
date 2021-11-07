from subprocess import CompletedProcess
from typing import Any
from camoulette.runner import Result, Runner
from camoulette.utils import BIN, _check_attribute, _get_or_exec, _get_ratio, _set_default_attribute
from . import Config
from .abstract_test import AbstractTest


class TestResult:

    name: str
    coef: float

    excepted: Result
    result: Result

    stdout_coef: float
    stderr_coef: float

    is_success: bool

    def __init__(self, name: str, coef: float,
                 excepted: Result, result: Result) -> None:
        self.coef = coef
        self.name = name
        self.result = result
        self.excepted = excepted
        self.is_valid = excepted == result
        self.stdout_coef = _get_ratio(excepted.stdout, result.stdout)
        self.stderr_coef = _get_ratio(excepted.stderr, result.stderr)

    def __str__(self) -> str:
        return f"{self.name}..." + ('OK' if self.is_valid else 'KO')

    def grade(self) -> float:
        return float(self.is_valid)


class Test(AbstractTest):

    coef: float
    program: str | Any
    return_code: bool
    stdout: str
    stderr: str

    def __init__(self) -> None:
        _check_attribute(self, "test")
        _set_default_attribute(self, "coef", 1.0)
        _set_default_attribute(self, "stderr", '')
        _set_default_attribute(self, "stdout", '')
        _set_default_attribute(self, "return_code", 2 if self.stderr else 0)
        super().__init__()

    def get_program(self, config: Config) -> str:
        program = ""
        for load in config.load:
            program += f"#use \"{load}\";;\n"
        program += _get_or_exec(config.prelude) + '\n'
        program += _get_or_exec(self.test) + '\n'
        return program

    def get_expected(self,
                     args: list[str],
                     program: str,
                     timeout: float) -> Result:
        return Result(
            CompletedProcess([], self.return_code, self.stdout, self.stderr),
            args, program, timeout, self.return_code
        )

    def get_args(self, config: Config) -> list[str]:
        args = [BIN]
        if not config.warning:
            args += ["-w", "-a-4-6-7-9-27-29-30-32..42-44-45-48-50-60-66-67-68"]
        args += _get_or_exec(config.extra_args)
        args += ['-I', config.path]
        return args + ["-stdin"]


    def run(self, config: Config) -> TestResult:
        self.
        args = self. get_args(config)
        program = self.get_program(config)
        timeout = _get_or_exec(config.timeout)

        runner = Runner(args, program, timeout)

        result = runner.run()
        expected = self.get_expected(args, program, timeout)

        return TestResult(self.name, self.coef, result, expected)
