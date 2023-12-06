from io import TextIOWrapper
from math import ceil, floor
import math

part1_test_input = """Time:      7  15   30
Distance:  9  40  200
"""

part1_test_output = 288


def part1(inp: TextIOWrapper):
    answer = 1

    # for line in inp.readlines():
    lines = [l for l in inp.readlines()]
    times = [int(x) for x in lines[0].split(":")[1].strip().split()]
    distances = [int(x) for x in lines[1].split(":")[1].strip().split()]

    for t, d in zip(times, distances):
        nums = 0
        for c in range(t):
            d2 = c * (t - c)
            if d2 > d:
                nums += 1
        answer *= nums

    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = 71503


def part2(inp: TextIOWrapper):
    answer = 1

    # for line in inp.readlines():
    lines = [l for l in inp.readlines()]
    times = [int(x) for x in lines[0].split(":")[1].replace(" ", "").split()]
    distances = [int(x) for x in lines[1].split(":")[1].replace(" ", "").split()]

    for t, d in zip(times, distances):
        # d2 = c * (t-c)
        # d2 / c = t - c
        # d2 = ct - cc
        # c**2 - t*c = -d2
        # c**2 - 2*(t/2)*c + (t/2)**2 = (t/2)**2 - d2
        # (c-t/2)**2 = (t/2)**2 - d2
        # c-(t/2) = +-sqrt(t/2**2 - d2)
        # c = +-sqrt(t/2**2 - d2) + t/2
        cmin = t / 2 - math.sqrt((t / 2) ** 2 - d) + t / 2
        cmax = t / 2 + math.sqrt((t / 2) ** 2 - d) + t / 2
        answer *= floor(cmax) - ceil(cmin) + 1

    return answer
