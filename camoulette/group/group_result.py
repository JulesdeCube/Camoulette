
from __future__ import annotations
from typing import Any

from camoulette.utils import WIDTH, normalize_code, to_block


class GroupResult:

    def __init__(self, group: Any, results: list[GroupResult]) -> None:
        self.group = group
        self.results = results

    @property
    def coef(self):
        return self.group.coef

    @property
    def height(self):
        return 1 + max(map(lambda t: t.height, self.results))

    def get_exercices(self):
        exercices = []
        if self.group.exercice:
            exercices.append(self)
        for result in self.results:
            exercices += result.get_exercices()
        return exercices

    @property
    def grade(self):
        if hasattr(self.group, 'grade'):
            return self.group.grade(self)
        coef = 0
        grade = 0
        for result in self.results:
            coef += result.coef
            grade += result.grade * result.coef
        return grade / coef

    def print(self, *, is_first=True, is_last=False, height=None):
        if height is None:
            height = self.height

        h = height
        if WIDTH > 160:
            h *= 2
            h += 1

        if is_first:
            print(f"┌{'─' * (WIDTH - 2)}┐")
        for _ in range(h):
            print(f"│ {' ' * (WIDTH - 4)} │")

        if self.group.exercice:
            color = '\033[34;1m'
        else:
            color = '\033[1m'
        grade = self.grade
        title = f"{self.group.name} [{grade:.3f}]"

        print(f"│ {color}{title.center(WIDTH - 4)}\033[0m │")

        for _ in range(h):
            print(f"│ {' ' * (WIDTH - 4)} │")

        if self.group.exercice and grade != 1:
            left = (WIDTH - 17) // 2
            right = WIDTH - 17 - left
            print(f"├{'─' * 13}┬{'─' * left}┬{'─' * right}┤")
            print(f"│{' ' * 13}│{'EXPECTED'.center(left)}│{'GOT'.center(right)}│")
            print(f"├{'─' * 13}┼{'─' * left}┼{'─' * right}┤")
            # print(f"├{'─' * 13}┼{'─' * left}┴{'─' * right}┤")
            print(to_block("CODE",
                           normalize_code(self.group.correction),
                           normalize_code("TODO"),
                           left, right), end='')
            print(f"├{'─' * 13}┴{'─' * left}┴{'─' * right}┤")
        else:
            print(f"├{'─' * (WIDTH - 2)}┤")

        if len(self.results):
            for result in self.results[:-1]:
                result.print(is_first=False,
                             height=height - 1)

            self.results[-1].print(is_first=False,
                                   is_last=is_last,
                                   height=height - 1)

        if is_last or is_first:
            print(f"└{'─' * (WIDTH - 2)}┘")

        if is_first:
            print()
            spacer = '\t\t'
            exercices = self.get_exercices()
            print(f"┌{'─' * (len(exercices) * 20 + 1)}┐")
            print("│", '│'.join(
                map(lambda res: f"{res.group.name[-20:]:>20}", exercices)), "│", sep='')
            print("│", ''.join(
                map(lambda res: f"{res.grade:0.4f}{spacer}", exercices)), " │")
            print(f"└{'─' * (len(exercices) * 20 + 1)}┘")
            print()
