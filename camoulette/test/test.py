from __future__ import annotations


from pathlib import Path
from camoulette.abc import AbcTest
from camoulette.file import File
from camoulette.ocaml import run_ocaml
from camoulette.test.test_result import TestResult
from camoulette.utils import BIN, set_default


class Test(AbcTest):

    __overwrite = {
        'returncode': 0,
        'stdout': '',
        'stderr': '',
    }

    returncode: int
    stdout: str
    stderr: str

    def __init__(self, *, parent: AbcTest = None) -> None:
        set_default(self, Test.__overwrite)

        super().__init__(parent=parent)

        if (not hasattr(self, 'test')):
            raise Exception(f"{self.name} test didn't have test")

    def get_program(self, path: Path, files: dict[str, File]) -> str:
        program = ""
        # TODO: make if better
        for load in self.load:
            program += f"#use \"{load}\";;\n"
            continue
            if load in files:
                program += files[load].get_content(files)
            else:
                try:
                    files[load] = File(Path(path) / load)
                except FileNotFoundError:
                    program += f"#use \"{load}\";;\n"
                else:
                    program += files[load].get_content(files)
        program += self.prelude + '\n'
        program += self.test + '\n'
        return program

    def get_args(self, path: Path) -> list[str]:
        args = [BIN]
        if not self.warning:
            args += ["-w", "-a-4-6-7-9-27-29-30-32..42-44-45-48-50-60-66-67-68"]
        args += self.extra_args
        args += ['-I', path]
        return args + ["-stdin"]

    def __call__(self, path: Path, *,
                 files: dict[str, File] = None) -> TestResult:
        if files is None:
            files = {}

        args = self.get_args(path)
        program = self.get_program(path, files)

        got = run_ocaml(args, program, self.timeout)
        return TestResult(self, got)
