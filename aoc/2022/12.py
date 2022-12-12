from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

part1_test_output = 31


def part1(inp: TextIOWrapper):
    answer = None

    m = [list(l.strip()) for l in inp.readlines()]

    start = None
    for y, row in enumerate(m):
        for x, h in enumerate(row):
            if h == "S":
                m[y][x] = "a"
                start = (y, x)

    assert start
    visited = set([start])
    queue = [[start]]
    width = len(m[0])
    height = len(m)
    while len(queue):
        path = queue.pop(0)
        y, x = path[-1]

        if m[y][x] == "E":
            return len(path) - 1
        for next_y, next_x in (y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1):
            if 0 <= next_x < width and 0 <= next_y < height:
                next_h = m[next_y][next_x]
                if next_h == "E":
                    next_h = "z"
                if ord(next_h) <= ord(m[y][x]) + 1 and (next_y, next_x) not in visited:
                    queue.append(path + [(next_y, next_x)])
                    visited.add((next_y, next_x))

    return answer


part2_test_input = part1_test_input

part2_test_output = 29


def part2(inp: TextIOWrapper):
    answer = None

    m = [list(l.strip()) for l in inp.readlines()]

    starts = []
    end = None
    for y, row in enumerate(m):
        for x, h in enumerate(row):
            if h == "S" or h == "a":
                m[y][x] = "a"
                starts.append((y, x))
            if h == "E":
                m[y][x] = "z"
                end = (y, x)

    width = len(m[0])
    height = len(m)

    assert len(starts)
    assert end
    shortest = width * height
    for start in starts:
        visited = set(start)
        queue = [[start]]
        while len(queue):
            path = queue.pop(0)
            y, x = path[-1]

            if (y, x) == end:
                if len(path) - 1 < shortest:
                    shortest = len(path) - 1
                    break

            for next_y, next_x in (y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1):
                if 0 <= next_x < width and 0 <= next_y < height:
                    next_h = m[next_y][next_x]
                    if (
                        ord(next_h) <= ord(m[y][x]) + 1
                        and (next_y, next_x) not in visited
                    ):
                        queue.append(path + [(next_y, next_x)])
                        visited.add((next_y, next_x))

    return shortest
