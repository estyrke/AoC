from collections import defaultdict
from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

part1_test_output = 26

IS_TEST: bool


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    sensors = {}
    beacons = defaultdict(set)
    target_row = 10 if IS_TEST else 2000000
    target_row_blocked = set()
    target_row_beacons = set()
    for tokens in parse_input(
        inp, "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"
    ):
        sx, sy, bx, by = tokens
        dist = abs(sx - bx) + abs(sy - by)
        y_dist = abs(sy - target_row)
        if target_row == by:
            target_row_beacons.add(bx)
        if y_dist <= dist:
            x_dist = dist - y_dist
            # print(sx, sy, bx, by, sx - x_dist, sx + x_dist + 1)

            for x in range(sx - x_dist, sx + x_dist + 1):
                target_row_blocked.add(x)
        sensors[(sx, sy)] = (bx, by)
        beacons[(bx, by)].add((sx, sy))

    answer = len(target_row_blocked.difference(target_row_beacons))
    assert answer != 5135730
    assert answer != 5135731

    return answer


part2_test_input = part1_test_input

part2_test_output = 56000011

from z3 import *


def part2(inp: TextIOWrapper):
    sensors = {}
    beacons = set()
    search_range = 20 if IS_TEST else 4000000
    blocked_ranges = [list() for y in range(search_range + 1)]

    for tokens in parse_input(
        inp, "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"
    ):
        sx, sy, bx, by = tokens
        dist = abs(sx - bx) + abs(sy - by)
        sensors[(sx, sy)] = dist
        beacons.add((bx, by))

    x, y = Int("x"), Int("y")
    s = Solver()
    s.add(x >= 0, x <= search_range)
    s.add(y >= 0, y <= search_range)
    for (sx, sy), d in sensors.items():
        dist = Abs(x - sx) + Abs(y - sy)
        s.add(dist > d)

    for bx, by in beacons:
        s.add((x, y) != (bx, by))

    print(s.check())
    m = s.model()
    x_s = m[x].as_long()
    y_s = m[y].as_long()
    print(x_s, y_s)
    return x_s * 4000000 + y_s
