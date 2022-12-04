from io import TextIOWrapper
import math
import functools
import itertools

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        ranges = line.strip().split(",")
        r1 = [int(x) for x in ranges[0].split("-")]
        r2 = [int(x) for x in ranges[1].split("-")]

        if r1[0] >= r2[0] and r1[1] <= r2[1] or r2[0] >= r1[0] and r2[1] <= r1[1]:
            answer += 1

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        ranges = line.strip().split(",")
        r1 = [int(x) for x in ranges[0].split("-")]
        r2 = [int(x) for x in ranges[1].split("-")]

        if r2[0] <= r1[1] and r2[1] >= r1[0] or r2[1] >= r1[0] and r2[0] <= r1[1]:
            answer += 1

    return answer
