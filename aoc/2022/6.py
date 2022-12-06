from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""

part1_test_output = 11


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]
    stream = list(inp.read().strip())

    recent = []
    for i, c in enumerate(stream):
        recent.append(c)
        if len(recent) > 4:
            recent.pop(0)
        if len(set(recent)) < 4:
            continue
        return i + 1


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    stream = list(inp.read().strip())

    recent = []
    for i, c in enumerate(stream):
        recent.append(c)
        if len(recent) > 14:
            recent.pop(0)
        if len(set(recent)) < 14:
            continue
        return i + 1
