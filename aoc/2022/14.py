from collections import defaultdict
from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

part1_test_output = 24


def part1(inp: TextIOWrapper):
    answer = 0

    cave = defaultdict(lambda: defaultdict(lambda: "."))

    min_x, max_x = 1000, -1
    min_y, max_y = 1000, -1

    for line in inp.readlines():
        coords = [x.split(",") for x in line.strip().split(" -> ")]
        ox, oy = -1, -1
        for coord in coords:
            nx, ny = int(coord[0]), int(coord[1])
            min_x, max_x = min(min_x, nx), max(max_x, nx)
            min_y, max_y = min(min_y, ny), max(max_y, ny)

            if ox >= 0:
                if ox == nx:
                    d = -1 if ny < oy else 1
                    for y in range(oy, ny + d, d):
                        cave[y][nx] = "#"
                else:
                    d = -1 if nx < ox else 1
                    for x in range(ox, nx + d, d):
                        cave[ny][x] = "#"
            ox, oy = (nx, ny)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(cave[y][x], end="")
        print()

    while True:
        sx, sy = (500, 0)
        while sy <= max_y:
            if cave[sy + 1][sx] == ".":
                sy += 1
            elif cave[sy + 1][sx - 1] == ".":
                sy += 1
                sx -= 1
            elif cave[sy + 1][sx + 1] == ".":
                sy += 1
                sx += 1
            else:
                cave[sy][sx] = "o"
                answer += 1
                break
        else:
            break

    return answer


part2_test_input = part1_test_input

part2_test_output = 93


def part2(inp: TextIOWrapper):
    answer = 0

    cave = defaultdict(lambda: defaultdict(lambda: "."))

    min_x, max_x = 1000, -1
    min_y, max_y = 1000, -1

    for line in inp.readlines():
        coords = [x.split(",") for x in line.strip().split(" -> ")]
        ox, oy = -1, -1
        for coord in coords:
            nx, ny = int(coord[0]), int(coord[1])
            min_x, max_x = min(min_x, nx), max(max_x, nx)
            min_y, max_y = min(min_y, ny), max(max_y, ny)

            if ox >= 0:
                if ox == nx:
                    d = -1 if ny < oy else 1
                    for y in range(oy, ny + d, d):
                        cave[y][nx] = "#"
                else:
                    d = -1 if nx < ox else 1
                    for x in range(ox, nx + d, d):
                        cave[ny][x] = "#"
            ox, oy = (nx, ny)

    cave[max_y + 2] = defaultdict(lambda: "#")
    max_y += 2

    while True:
        sx, sy = (500, 0)
        if cave[sy][sx] == "o":
            break
        while sy <= max_y:
            if cave[sy + 1][sx] == ".":
                sy += 1
            elif cave[sy + 1][sx - 1] == ".":
                sy += 1
                sx -= 1
            elif cave[sy + 1][sx + 1] == ".":
                sy += 1
                sx += 1
            else:
                cave[sy][sx] = "o"
                answer += 1
                break
        else:
            break

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(cave[y][x], end="")
        print()

    return answer
