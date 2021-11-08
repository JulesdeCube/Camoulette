from typing import Any
from camoulette.ocaml import Result

from camoulette.utils import CROP, FLEXIBLE, WIDTH, color_len, normalize_code, similar, to_block, to_one_block


class TestResult:

    def __init__(self, test: Any, result: Result) -> None:
        self.test = test
        self.result = result

    @ property
    def stdout_ratio(self):
        got = self.result.stdout
        if self.test.mode == CROP:
            return similar(self.test.stdout, got[:len(self.test.stdout)])
        elif self.test.mode == FLEXIBLE:
            return similar(self.test.stdout, got)
        else:
            return int(self.test.stdout == got)

    @property
    def height(self):
        return -1

    @ property
    def stderr_ratio(self):
        got = self.result.stderr
        if self.test.mode == CROP:
            return similar(self.test.stderr, got[:len(self.test.stderr)])
        elif self.test.mode == FLEXIBLE:
            return similar(self.test.stderr, got)
        else:
            return int(self.test.stderr == got)

    @ property
    def coef(self):
        return self.test.coef

    @ property
    def grade(self):
        if hasattr(self.test, 'grade'):
            return self.test.grade(self)

        if self.result.as_timeout:
            return 0
        if self.result.returncode != self.test.returncode:
            return 0
        coef = 0
        grade = 0
        if self.test.stdout != '':
            coef += 1
            grade += self.stdout_ratio
        if self.test.stderr != '':
            coef += 1
            grade += self.stderr_ratio
        if coef:
            return grade / coef * self.result.grade
        else:
            return float(self.result.stdout ==
                         '' and self.result.stderr == '') * self.result.grade

    def get_exercices(self):
        return []

    def print(self, *, is_first=True, is_last=False, **kwargs):
        grade = self.grade

        if grade == 1:
            color = 32
        elif grade == 0:
            color = 31
        else:
            color = 33

        to_print = f'{self.test.name}\033[2m...\033[0;{color}m{grade:.2f}\033[0m'
        if self.result.as_timeout:
            to_print += f" (\033[33;1;7;5mTIMEOUT {self.result.timeout}s\033[0m)"
        else:
            to_print += f" (\033[33m{self.result.time:.2f}s\033[0m)"
        to_print += ' ' * (WIDTH - color_len(to_print) - 2)
        print(f"│{to_print}│")
        if grade != 1 and not self.result.as_timeout:
            left = (WIDTH - 17) // 2
            right = WIDTH - 17 - left
            print(f"├{'─' * 13}┬{'─' * (WIDTH - 16)}┤")
            print(
                to_one_block(
                    "TEST",
                    normalize_code(
                        self.test.test),
                    WIDTH),
                end='')
            print(f"├{'─' * 13}┼{'─' * left}┬{'─' * right}┤")
            print(
                f"│{' ' * 13}│{'EXPECTED'.center(left)}│{'GOT'.center(right)}│")
            # print(f"├{'─' * 13}┼{'─' * left}┴{'─' * right}┤")

            bef = f"├{'─' * 13}┼{'─' * left}┼{'─' * right}┤"
            if self.test.returncode != self.result.returncode:
                print(bef)
                print(to_block("RESULT CODE",
                               self.test.returncode, self.result.returncode,
                               left, right), end='')

            if self.stdout_ratio != 1:
                print(bef)
                print(to_block("STDOUT",
                               self.test.stdout, self.result.stdout,
                               left, right), end='')

            if self.stderr_ratio != 1:
                print(bef)
                print(to_block("STDERR",
                               self.test.stderr, self.result.stderr,
                               left, right), end='')

            if is_last:
                print(f"└{'─' * 13}┴{'─' * left}┴{'─' * right}┘")
            else:
                print(f"├{'─' * 13}┴{'─' * left}┴{'─' * right}┤")

        elif is_last:
            print(f"└{'─' * (WIDTH - 2)}┘")
