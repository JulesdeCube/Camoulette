from difflib import SequenceMatcher
import os

import sys


BIN = "/nix/store/6jsqrblnldrkwm8l0l10yrh29z9sb0g1-ocaml-4.12.0/bin/ocaml"

STRICT = 1
CROP = 2
FLEXIBLE = 3


def color_len(string: str) -> int:
    l = 0
    espace = False
    for c in string:
        if espace:
            espace = c != 'm'
        else:
            espace = c == '\033'
            l += int(not espace)
    return l


def get_width():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                   '1234'))
        except BaseException:
            return None

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except BaseException:
            pass

    return int(cr[1]) if cr else 160


WIDTH = get_width()


def similar(a, b):
    return min(SequenceMatcher(None, a, b).ratio(),
               SequenceMatcher(None, b, a).ratio())


def set_default(src: object, comp: dict):
    for key, value in comp.items():
        if not hasattr(src, key):
            src.__dict__[key] = value


def heredity(src: object, comp: object):
    for key in dir(comp):
        if not hasattr(src, key):
            src.__dict__[key] = comp.__getattribute__(key)


def wrap_lines(lines: list[str], size: int) -> list[str]:
    wraps_lines = []
    for line in lines:
        if line == '':
            wraps_lines.append('¶')

        wraps = [line[i:i + size - 1] for i in range(0, len(line), size - 1)]
        for i in range(len(wraps)):
            wraps[i] += "↵" if i != len(wraps) - 1 else '¶'
        wraps_lines += wraps
    return wraps_lines


def to_block(name: str, excepted: str, got: str, left: int, right: int):
    got = str(got)
    excepted = str(excepted)
    s = ""
    ex_lines = wrap_lines(excepted.splitlines(), left - 1)
    got_lines = wrap_lines(got.splitlines(), right - 1)
    l = max(len(ex_lines), len(got_lines))
    for i in range(0, max(1, l)):
        n = name if i == 0 else ''
        ex_l = ex_lines[i] if i < len(ex_lines) else ''
        got_l = got_lines[i] if i < len(got_lines) else ''
        s += f"│ {n:<11} │ {ex_l.ljust(left-1)}│ {got_l.ljust(right-1)}│\n"
    return s


def to_one_block(name: str, content: str, size: int):
    content = str(content)
    lines = wrap_lines(content.splitlines(), size - 17)
    if lines == []:
        lines = ['']
    s = ""
    for i, line in enumerate(lines):
        n = name if i == 0 else ''
        s += f"│ {n:<11} │ {line.ljust(size - 17)}│\n"
    return s


def normalize_code(code: str):
    lines = code.splitlines()

    start = sys.maxsize
    for line in lines:
        if not line:
            continue
        s = 0
        for c in line:
            if not c.isspace():
                break
            s += 1
        start = min(start, s)

    lines = [line[start:] for line in lines]

    l = ''
    while lines and (l := lines.pop()) == '':
        continue
    lines.append(l)

    l = ''
    while lines and (l := lines.pop(0)) == '':
        continue
    lines.insert(0, l)

    return '\n'.join(lines)
