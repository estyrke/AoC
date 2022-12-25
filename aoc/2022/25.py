from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

part1_test_output = "2=-1=0"


conv = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def decode(inp: str) -> int:
    num = 0
    for i, ch in enumerate(inp):
        num *= 5
        num += conv[ch]
    return num


def encode(inp: int) -> str:
    res = ""
    while inp > 0:
        inp, dig = divmod(inp, 5)
        res = "012=-"[dig] + res
        if dig > 2:
            inp += 1
    return res


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        answer += decode(line.strip())

    return encode(answer)


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = None

    return answer
