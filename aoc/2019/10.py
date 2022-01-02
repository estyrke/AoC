from io import TextIOWrapper
import math
import itertools
import functools
from typing import List, Tuple

part1_test_input = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

part1_test_output = 210


@functools.cache
def valid_dx(dy: int, x: int, w: int):
    def gen():
        if dy == 0:
            if x > 0:
                yield -1
            if x < w - 1:
                yield 1
        else:
            if dy in [-1, 1]:
                yield 0
            for i in itertools.islice(itertools.count(1), 33):
                if math.gcd(dy, i) == 1:
                    if x + i < w:
                        yield i
                    if x - i >= 0:
                        yield -i

    return list(gen())


def clockwise_order(d: Tuple[int, int]) -> float:
    """
    >>> clockwise_order((1, 0)) / 2 / math.pi * 360
    90.0
    >>> clockwise_order((0, 1)) / 2 / math.pi * 360
    180.0
    >>> clockwise_order((-1, 0)) / 2 / math.pi * 360
    270.0
    >>> clockwise_order((0, -1)) / 2 / math.pi * 360
    0.0
    """
    dx, dy = d
    return (-math.atan2(-dy, dx) + math.pi / 2) % (2 * math.pi)


@functools.cache
def rotation(x, y, w, h):
    deltas = []
    for dy in range(-y, h - y):
        for dx in valid_dx(dy, x, w):
            deltas.append((dx, dy))

    deltas.sort(key=clockwise_order)

    return deltas


def visible(map, x: int, y: int, w: int, h: int) -> int:
    v = 0
    for dx, dy in rotation(x, y, w, h):
        for i in itertools.count(1):
            ny = y + dy * i
            nx = x + dx * i
            if not 0 <= ny < h or not 0 <= nx < w:
                break
            if map[ny][nx] == "#":
                v += 1
                break
    return v


def vaporized(map, x: int, y: int, w: int, h: int) -> List[Tuple[int, int]]:
    v = []
    for dx, dy in rotation(x, y, w, h):
        for i in itertools.count(1):
            ny = y + dy * i
            nx = x + dx * i
            if not 0 <= ny < h or not 0 <= nx < w:
                break
            if map[ny][nx] == "#":
                v.append((nx, ny))
                break
    return v


def part1(inp: TextIOWrapper):
    lines = [list(l.strip()) for l in inp.readlines()]
    h = len(lines)
    w = len(lines[0])
    best = (0, 0, 0)
    for y, l in enumerate(lines):
        for x, p in enumerate(l):
            if p == "#":
                v = visible(lines, x, y, w, h)
                if v > best[2]:
                    best = (x, y, v)

    print(best)
    return best[2]


part2_test_input = part1_test_input

part2_test_output = 802


def part2(inp: TextIOWrapper):
    lines = [list(l.strip()) for l in inp.readlines()]
    h = len(lines)
    w = len(lines[0])

    best = (0, 0, 0)
    for y, l in enumerate(lines):
        for x, p in enumerate(l):
            if p == "#":
                v = visible(lines, x, y, w, h)
                if v > best[2]:
                    best = (x, y, v)
    v = []
    x, y, _ = best
    print(best)
    while len(v) < 200:
        new_v = vaporized(lines, x, y, w, h)
        v += new_v
        for (x, y) in new_v:
            lines[y][x] = "."

    return v[199][0] * 100 + v[199][1]
