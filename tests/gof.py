from __future__ import annotations


def one_of_2(string: str) -> str:
    def o_of_t(line: str):
        s = ""
        for i in range(0, len(line), 2):
            s += line[i]
        return s

    return '\n'.join(map(o_of_t, string.splitlines()))


class Board:
    def __init__(self, board: list[list[int]]):
        self.__board = board

    @staticmethod
    def from_size(size: int):
        Board([[0] * size for _ in range(size)])

    @staticmethod
    def from_str(string: str) -> Board:
        if '█' in string:
            string = one_of_2(string)

        def cell_from_c(c: str) -> int:
            return int(c == 'X' or c == '1' or c == '█')

        return Board([
            list(map(cell_from_c, line))
            for line in string.splitlines()
            if line
        ])

    @property
    def w(self):
        return len(self.__board[0]) if self.__board else 0

    @property
    def h(self):
        return len(self.__board)

    def get_adj(self, x: int, y: int) -> int:
        def sum_line(l: list[int]):
            return sum(l[max(0, x - 1): x + 2])
        s = sum(map(sum_line, self.__board[max(0, y - 1): y + 2]))
        return s - self.__board[y][x]

    def next_state(self, x: int, y: int) -> int:
        s = self.get_adj(x, y)
        return s == 3 or (self.__board[y][x] and s == 2)

    def next_gen(self):
        return Board([
            [
                self.next_state(x, y)
                for x in range(self.w)
            ]
            for y in range(self.h)
        ])

    def clone(self) -> Board:
        return Board([
            [
                self.next_state(x, y)
                for x in range(self.w)
            ]
            for y in range(self.h)
        ])

    def __str__(self) -> str:
        def cell_str(c: int):
            return '██' if c else '  '

        def line_str(l: list[int]):
            return ''.join(map(cell_str, l))

        return '\n'.join(map(line_str, self.__board))


# board1 = Board.from_str("""
# 0010001011
# 0110110110
# 1101101101
# 0001000100
# 0101100001
# """)

# board2 = Board.from_str(
#     "    ██      ██  ████\n"
#     "  ████  ████  ████  \n"
#     "████  ████  ████  ██\n"
#     "      ██      ██    \n"
#     "  ██  ████        ██\n"
# )


# print(board1)
# print()
# print(board2.next_gen())
