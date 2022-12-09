from io import TextIOWrapper
import math
import functools
import itertools
from pprint import pprint
from typing import List, Tuple
from ..tools import parse_input

part1_test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

part1_test_output = 13


def move(pos, dir, amount):
    assert amount == 1
    if dir == "R":
        return (pos[0] + 1, pos[1])
    elif dir == "L":
        return (pos[0] - 1, pos[1])
    elif dir == "U":
        return (pos[0], pos[1] + 1)
    elif dir == "D":
        return (pos[0], pos[1] - 1)
    assert False


def sign(num):
    assert num != 0
    return 1 if num > 0 else -1


def follow(head, tail):
    assert -2 <= (head[0] - tail[0]) <= 2
    assert -2 <= (head[1] - tail[1]) <= 2

    if (head[0] - tail[0]) == 2 and head[1] == tail[1]:
        assert -1 <= (head[1] - tail[1]) <= 1
        return (tail[0] + 1, head[1])
    elif (head[0] - tail[0]) == -2 and head[1] == tail[1]:
        assert -1 <= (head[1] - tail[1]) <= 1
        return (tail[0] - 1, head[1])
    elif (head[1] - tail[1]) == 2 and head[0] == tail[0]:
        assert -1 <= (head[0] - tail[0]) <= 1
        return (head[0], tail[1] + 1)
    elif (head[1] - tail[1]) == -2 and head[0] == tail[0]:
        assert -1 <= (head[0] - tail[0]) <= 1
        return (head[0], tail[1] - 1)

    x, y = tail
    if (head[0] - tail[0]) == 2:
        assert -2 <= (head[1] - tail[1]) <= 2
        return (x + 1, y + sign(head[1] - y))
    elif (head[0] - tail[0]) == -2:
        assert -2 <= (head[1] - tail[1]) <= 2
        return (x - 1, y + sign(head[1] - y))

    if (head[1] - tail[1]) == 2:
        assert -2 <= (head[0] - tail[0]) <= 2
        return (x + sign(head[0] - x), y + 1)
    elif (head[1] - tail[1]) == -2:
        assert -2 <= (head[0] - tail[0]) <= 2
        return (x + sign(head[0] - x), y - 1)

    assert -1 <= (head[0] - x) <= 1
    assert -1 <= (head[1] - y) <= 1

    return (x, y)


def part1(inp: TextIOWrapper):
    answer = 1

    H = (0, 0)
    T = (0, 0)
    tTrail = set()
    tTrail.add(T)

    for line in inp.readlines():
        dir, amount = line.strip().split()
        amount = int(amount)

        for n in range(amount):
            H = move(H, dir, 1)
            T = follow(H, T)
            # print(H, T)
            tTrail.add(T)
        # print()
        # pprint(tTrail)

    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return len(tTrail)


part2_test_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

part2_test_output = 36


def part2(inp: TextIOWrapper):
    knots: List[Tuple[int, int]] = [(0, 0) for _ in range(10)]
    tTrail = set()
    tTrail.add(knots[-1])

    for line in inp.readlines():
        dir, amount = line.strip().split()
        amount = int(amount)

        for n in range(amount):
            knots[0] = move(knots[0], dir, 1)
            for i in range(1, 10):
                knots[i] = follow(knots[i - 1], knots[i])
            tTrail.add(knots[-1])
        # print()
        # pprint(tTrail)

    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    answer = len(tTrail)
    assert answer != 2414
    return answer
