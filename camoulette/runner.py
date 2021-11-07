from os import times
import time
import subprocess

from camoulette.utils import _set_default_attribute


class Result:

    args: list[str]
    program: str

    returncode: int
    stdout: str
    stderr: str

    timeout: float
    time: float

    def __init__(self,
                 result: subprocess.CompletedProcess | subprocess.TimeoutExpired,
                 args: list[str],
                 program: str,
                 timeout: float,
                 time: float) -> None:
        self.program = program
        self.args = args

        _set_default_attribute(result, "returncode", 0)

        self.returncode = result.returncode
        self.stdout = str(result.stdout)
        self.stderr = str(result.stderr)

        self.timeout = timeout
        self.time = time

    @property
    def as_timeout(self):
        return self.timeout == self.time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Result):
            return False

        if self.as_timeout != other.as_timeout:
            return False

        if self.returncode != other.returncode:
            return False

        if self.stdout != other.stdout:
            return False

        if self.stderr == '':
            return other.stderr == ''
        else:
            return other.stdout.startswith(self.stderr)

    def __str__(self) -> str:
        return str(self)


class Runner:

    args: list[str]
    progam: str
    timeout: float

    def __init__(self, args: list[str], program: str, timeout: float) -> None:
        self.args = args
        self.progam = program
        self.timeout = timeout

    def run(self) -> Result:
        try:
            start = time.time_ns()
            sub_proc = subprocess.run(self.args,
                                      text=True,
                                      input=self.progam,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      timeout=self.timeout)
            end = time.time_ns()
        except subprocess.TimeoutExpired as sub_proc:
            proc_time = self.timeout
        else:
            proc_time = end - start

        return Result(sub_proc,
                      self.args,
                      self.progam,
                      self.timeout,
                      proc_time)
