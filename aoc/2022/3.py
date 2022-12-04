from io import TextIOWrapper
import math
import functools
import itertools

part1_test_input = """"""

part1_test_output = None


def prio(c: str) -> int:
    if "a" <= c <= "z":
        return ord(c) - ord("a") + 1
    elif "A" <= c <= "Z":
        return ord(c) - ord("A") + 27
    assert False


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        line = line.strip()
        c1 = set(line[: len(line) // 2])
        c2 = set(line[len(line) // 2 :])
        dup = c1.intersection(c2)
        assert len(dup) == 1
        answer += prio(dup.pop())

    # lines = [l for l in inp.readlines()]

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = 0

    lines = [l for l in inp.readlines()]

    for i in range(len(lines) // 3):
        c = [set(lines[i * 3 + j].strip()) for j in range(3)]
        dup1 = c[0].intersection(c[1])
        dup = dup1.intersection(c[2])
        assert len(dup) == 1
        answer += prio(dup.pop())

    return answer
