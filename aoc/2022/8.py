from io import TextIOWrapper
import math
import functools
import itertools
from pprint import pprint
from ..tools import parse_input

part1_test_input = """30373
25512
65332
33549
35390
"""

part1_test_output = 21


def part1(inp: TextIOWrapper):
    grid = [list(map(int, list(l.strip()))) for l in inp.readlines()]
    visible = []
    for y, row in enumerate(grid):
        max_h = -1

        visible.append(list())
        for x, h in enumerate(row):
            if h > max_h:
                max_h = h
                visible[y].append(True)

            else:
                visible[y].append(False)
        max_h = -1
        for x, h in reversed(list(enumerate(row))):
            if h > max_h:
                max_h = h
                visible[y][x] = True
    for x in range(len(grid[0])):
        max_h = -1
        for y in range(len(grid)):
            h = grid[y][x]
            if h > max_h:
                max_h = h
                visible[y][x] = True
        max_h = -1
        for y in range(len(grid) - 1, -1, -1):
            assert y >= 0
            assert y < len(grid)
            h = grid[y][x]
            if h > max_h:
                max_h = h
                visible[y][x] = True
    # pprint(visible)
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return sum([sum(row) for row in visible])


part2_test_input = part1_test_input

part2_test_output = 8


def dist(x, y, grid):
    d = 1
    h = grid[y][x]
    height = len(grid)
    width = len(grid[0])
    if x == 0 or y == 0 or x == width - 1 or y == height - 1:
        return 0
    for c in range(x + 1, width):
        if h <= grid[y][c]:
            break
    d *= c - x
    for c in range(x - 1, -1, -1):
        if h <= grid[y][c]:
            break
    d *= abs(c - x)

    for r in range(y + 1, height):
        if h <= grid[r][x]:
            break
    d *= r - y

    for r in range(y - 1, -1, -1):
        if h <= grid[r][x]:
            break
    d *= abs(r - y)
    return d


def part2(inp: TextIOWrapper):
    grid = [list(map(int, list(l.strip()))) for l in inp.readlines()]
    visible = []

    for y, row in enumerate(grid):
        visible.append(list())
        for x, h in enumerate(row):
            visible[y].append(dist(x, y, grid))

    pprint(visible)
    answer = max([max(row) for row in visible])
    assert answer != 2706
    return answer
    for y, row in enumerate(grid):
        visible.append(list())
        for x, h in enumerate(row):
            if x == 0:
                visible[y].append(0)
            elif h > grid[y][x - 1]:
                visible[y].append(visible[y][x - 1] + 1)
            else:
                visible[y].append(1)
        for x, h in reversed(list(enumerate(row))):
            if x == len(row) - 1:
                visible[y][x] = 0
            elif h > grid[y][x + 1]:
                visible[y][x] *= visible[y][x + 1] + 1
            else:
                visible[y][x] *= 1
    # pprint(visible)
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            h = grid[y][x]
            if y == 0:
                visible[y][x] = 0
            elif h > grid[y - 1][x]:
                visible[y][x] *= visible[y - 1][x] + 1
            else:
                visible[y][x] *= 1
        for y in range(len(grid) - 1, -1, -1):
            h = grid[y][x]
            if y == len(grid) - 1:
                visible[y][x] = 0
            elif h > grid[y + 1][x]:
                visible[y][x] *= visible[y + 1][x] + 1
            else:
                visible[y][x] *= 1
    pprint(visible)
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    answer = max([max(row) for row in visible])
    assert answer != 2706
    return answer
