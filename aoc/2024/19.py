from functools import cache
from io import StringIO, TextIOBase
import sys

part1_test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

part1_test_output = 6


@cache
def check_design(patterns, design):
    matches = 0
    for p in patterns:
        if design == p:
            matches += 1
        elif design.startswith(p):
            matches += check_design(patterns, design[len(p) :])
    return matches


def part1(inp: TextIOBase):
    answer = None

    patterns, designs = inp.read().split("\n\n")
    patterns = tuple(patterns.strip().split(", "))
    designs = designs.strip().split("\n")

    answer = 0
    for d in designs:
        answer += 1 if check_design(patterns, d) else 0
    return answer


part2_test_input = part1_test_input

part2_test_output = 16


def part2(inp: TextIOBase):
    answer = None

    patterns, designs = inp.read().split("\n\n")
    patterns = tuple(patterns.strip().split(", "))
    designs = designs.strip().split("\n")

    answer = 0
    for d in designs:
        new = check_design(patterns, d)
        answer += new
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
