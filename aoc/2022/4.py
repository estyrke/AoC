from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = 0

    for r1x, r1y, r2x, r2y in parse_input(inp, "{:d}-{:d},{:d}-{:d}"):

        if r1x >= r2x and r1y <= r2y or r2x >= r1x and r2y <= r1y:
            answer += 1

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = 0

    for r1x, r1y, r2x, r2y in parse_input(inp, "{:d}-{:d},{:d}-{:d}"):
        if r2x <= r1y and r2y >= r1x or r2y >= r1x and r2x <= r1y:
            answer += 1

    return answer
