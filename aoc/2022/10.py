from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input
from advent_of_code_ocr import convert_6

part1_test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

part1_test_output = 13140


def part1(inp: TextIOWrapper):
    x = 1
    values = [1]
    for line in inp.readlines():
        inst = line.strip().split()
        if inst[0] == "noop":
            values.append(x)
        elif inst[0] == "addx":
            values.extend([x, x])
            x += int(inst[1])

    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]
    answer = 0
    for cycle in range(20, len(values), 40):
        answer += values[cycle] * cycle
    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = None

    x = 1
    values = []
    for line in inp.readlines():
        inst = line.strip().split()
        if inst[0] == "noop":
            values.append(x)
        elif inst[0] == "addx":
            values.extend([x, x])
            x += int(inst[1])

    screen = ""
    for c, x in enumerate(values):
        pos = c % 40

        if c > 0 and pos % 40 == 0:
            screen += "\n"

        if x - 1 <= pos <= x + 1:
            screen += "#"
        else:
            screen += "."

    print(screen)
    try:
        return convert_6(screen)
    except KeyError:  # conversion fails for the test input
        print("Unable to convert!")
        return None
