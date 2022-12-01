from io import TextIOWrapper
import math
import functools
import itertools

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = 0
    curr = 0
    for line in inp.readlines():
        if line.strip() == "":
            if curr > answer:
                answer = curr
            curr = 0
        else:
            curr += int(line)

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    curr = 0
    maxes = [0, 0, 0]
    for line in inp.readlines():
        if line.strip() == "":
            if curr > maxes[0]:
                maxes.append(curr)
                maxes.sort()
                maxes.pop(0)
            curr = 0
        else:
            curr += int(line)

    return sum(maxes)
