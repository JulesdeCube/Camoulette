from __future__ import annotations

import re

from io import TextIOWrapper
from pathlib import Path

# not a prety regex but work
use_regex = re.compile("#use \"([a-zA-Z_/-]+.ml)\"")


class File:
    path: Path
    blocks: list[str]

    def __init__(self, path: Path) -> None:
        self.path = path
        file = open(path)
        content = '\n'.join(file.readlines())
        file.close()

        blocks = content.split(';;')
        self.blocks = [block.strip() + ';;' for block in blocks]

    def get_content(self, files: list[File]) -> str:
        content = ''
        for block in self.blocks:
            use = use_regex.match(block.splitlines()[-1])
            if use:
                print()
        return content