from io import TextIOWrapper
import math
import functools
import itertools
from pprint import pprint
from typing import Dict, Tuple
from ..tools import parse_input

part1_test_input = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""
part1_test_input2 = """.....
..##.
..#..
.....
..##.
....."""

part1_test_output = 110


def part1(inp: TextIOWrapper):
    map: Dict[Tuple[int, int], Tuple[int, int]] = {}
    max_x = max_y = 0
    min_x = min_y = math.inf
    lines = [list(l.strip()) for l in inp.readlines()]
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "#":
                map[(y, x)] = (y, x)
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    # print(map)

    dirs = [
        [(-1, 0), (-1, -1), (-1, 1)],
        [(1, 0), (1, -1), (1, 1)],
        [(0, -1), (-1, -1), (1, -1)],
        [(0, 1), (-1, 1), (1, 1)],
    ]

    all_dirs = [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]
    dir_idx = 0
    for i in range(10):
        move = False
        for k, v in map.items():
            for d in all_dirs:
                if add(k, d) in map:
                    for p_dir in range(4):
                        dir, p_dir1, p_dir2 = dirs[(dir_idx + p_dir) % 4]
                        if (
                            add(k, dir) not in map
                            and add(k, p_dir1) not in map
                            and add(k, p_dir2) not in map
                        ):
                            map[k] = add(k, dir)
                            move = True
                            break
                    else:
                        map[k] = k
                    break
            else:
                map[k] = k

        if not move:
            print("Stable position")
            break
        dir_idx = (dir_idx + 1) % len(dirs)

        map2: Dict[Tuple[int, int], Tuple[int, int]] = {}
        for f, t in map.items():
            if t in map2:
                map2[map2[t]] = map2[t]
                del map2[t]
                map2[f] = f
            else:
                map2[t] = f

        map = map2

    for y, x in map.keys():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    print(min_x, max_x, min_y, max_y)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(map)


def print_map(map):
    min_x = min_y = 1000 * 1000 * 1000
    max_x = max_y = 0
    for y, x in map.keys():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            if (y, x) in map:
                print("#", end="")
            else:
                print(".", end="")
        print()


def add(pos: Tuple[int, int], diff: Tuple[int, int]):
    return pos[0] + diff[0], pos[1] + diff[1]


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    map: Dict[Tuple[int, int], Tuple[int, int]] = {}
    max_x = max_y = 0
    min_x = min_y = math.inf
    lines = [list(l.strip()) for l in inp.readlines()]
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == "#":
                map[(y, x)] = (y, x)
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    # print(map)

    dirs = [
        [(-1, 0), (-1, -1), (-1, 1)],
        [(1, 0), (1, -1), (1, 1)],
        [(0, -1), (-1, -1), (1, -1)],
        [(0, 1), (-1, 1), (1, 1)],
    ]

    all_dirs = [(-1, 0), (-1, -1), (-1, 1), (1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]
    dir_idx = 0
    round = 0
    while True:
        round += 1
        move = False
        for k, v in map.items():
            for d in all_dirs:
                if add(k, d) in map:
                    for p_dir in range(4):
                        dir, p_dir1, p_dir2 = dirs[(dir_idx + p_dir) % 4]
                        if (
                            add(k, dir) not in map
                            and add(k, p_dir1) not in map
                            and add(k, p_dir2) not in map
                        ):
                            map[k] = add(k, dir)
                            move = True
                            break
                    else:
                        map[k] = k
                    break
            else:
                map[k] = k

        if not move:
            print("Stable position", round)
            return round
        dir_idx = (dir_idx + 1) % len(dirs)

        map2: Dict[Tuple[int, int], Tuple[int, int]] = {}
        for f, t in map.items():
            if t in map2:
                map2[map2[t]] = map2[t]
                del map2[t]
                map2[f] = f
            else:
                map2[t] = f

        map = map2
