from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input
from typing import cast
from parse import parse

part1_test_input = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

part1_test_output = "CMZ"


def part1(inp: TextIOWrapper):
    stacks: list[list[str]] = []

    moves = False
    for line in inp.readlines():
        if not line.strip():
            moves = True
            continue

        if moves:
            print(line)
            n, from_stack, to_stack = parse(
                "move {:d} from {:d} to {:d}", line.strip()
            ).fixed
            move = stacks[from_stack - 1][:n]
            stacks[to_stack - 1][0:0] = reversed(move)
            stacks[from_stack - 1][:n] = []
            print(stacks)
        else:
            nstacks = len(line) // 4
            if len(stacks) < nstacks:
                stacks.extend([list() for _ in range(nstacks - len(stacks))])
            for s in range(nstacks):
                # print(s * 4 + 1, line, line[s * 4 + 1])
                if s * 4 + 1 < len(line) and "A" <= line[s * 4 + 1] <= "Z":
                    stacks[s].append(line[s * 4 + 1])

    return "".join([s[0] if len(s) else "!" for s in stacks])


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    stacks: list[list[str]] = []

    moves = False
    for line in inp.readlines():
        if not line.strip():
            moves = True
            continue

        if moves:
            print(line)
            n, from_stack, to_stack = parse(
                "move {:d} from {:d} to {:d}", line.strip()
            ).fixed
            move = stacks[from_stack - 1][:n]
            stacks[to_stack - 1][0:0] = move
            stacks[from_stack - 1][:n] = []
            print(stacks)
        else:
            nstacks = len(line) // 4
            if len(stacks) < nstacks:
                stacks.extend([list() for _ in range(nstacks - len(stacks))])
            for s in range(nstacks):
                # print(s * 4 + 1, line, line[s * 4 + 1])
                if s * 4 + 1 < len(line) and "A" <= line[s * 4 + 1] <= "Z":
                    stacks[s].append(line[s * 4 + 1])

    return "".join([s[0] if len(s) else "!" for s in stacks])
