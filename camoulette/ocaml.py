import subprocess
import time


class Result:

    def __init__(self, args: list[str], program: str, timeout: float,
                 returncode: int, stdout: str, stderr: str, time: float) -> None:
        self.program = program
        self.args = args
        self.timeout = timeout
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.time = time

    @ property
    def grade(self) -> float:
        return float(not self.as_timeout) * self.efficiency

    @ property
    def as_timeout(self) -> bool:
        return self.returncode == -1

    @ property
    def efficiency(self) -> bool:
        return min(1, 1 - ((self.time - 0.05) / self.timeout)) ** 2


def run_ocaml(args, program, timeout) -> Result:
    try:
        start = time.time()
        res = subprocess.run(args,
                             text=True,
                             input=program,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             timeout=timeout)
        end = time.time()
    except subprocess.TimeoutExpired as err:
        return Result(args, program, timeout, -1,
                      err.stdout, err.stderr, timeout)
    else:
        return Result(args, program, timeout, res.returncode,
                      res.stdout, res.stderr, end - start)
