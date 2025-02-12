from io import TextIOBase
from typing import cast
import parse


def parse_input(inp: TextIOBase, pattern: str):
    parser = parse.compile(pattern)
    for line in inp.readlines():
        result = parser.parse(line.strip())
        if result is None:
            raise RuntimeError(f"Failed to parse input line {line} using pattern {pattern}")
        yield cast(parse.Result, result).fixed
