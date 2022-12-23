from enum import Enum
from io import TextIOWrapper
import math
import functools
import itertools
from typing import Dict, List, Tuple
from ..tools import parse_input
import re
import numpy as np


part1_test_input = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


part1_test_output = 6032


def move(
    map: List[List[str]], pos: Tuple[int, int], dir: Tuple[int, int], amount: int
) -> Tuple[int, int]:
    last_ok_pos = pos
    while amount > 0:
        new_pos = pos[0] + dir[0], pos[1] + dir[1]
        if dir[0] != 0:
            if new_pos[0] < 0:
                new_pos = len(map[new_pos[1]]) - 1, new_pos[1]
            elif new_pos[0] >= len(map[new_pos[1]]):
                new_pos = 0, new_pos[1]
        else:
            assert dir[1] != 0
            if new_pos[1] < 0:
                new_pos = new_pos[0], len(map) - 1
            elif new_pos[1] >= len(map):
                new_pos = new_pos[0], 0
        try:
            char = map[new_pos[1]][new_pos[0]]
        except:
            print(new_pos[0], new_pos[1])
            raise
        if char == "#":
            break
        elif char == ".":
            amount -= 1
            last_ok_pos = new_pos
        pos = new_pos

    return last_ok_pos


def rotate(dir: int, turn: str):
    if turn == "L":
        return (dir - 1) % 4
    else:
        assert turn == "R"
        return (dir + 1) % 4


def part1(inp: TextIOWrapper):
    answer = None

    map, path = inp.read().split("\n\n")
    map = [list(r) for r in map.split("\n")]
    max_w = max(len(r) for r in map)

    for i in map:
        i += [" "] * (max_w - len(i))
        print(len(i))
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dir = 0

    pos = (0, 0)
    while map[pos[1]][pos[0]] == " ":
        pos = (pos[0] + 1, pos[1])

    for m in re.finditer("(\d+)([LR])?", path):
        amount, turn = m.groups()
        amount = int(amount)
        # print(amount, turn)

        pos = move(map, pos, dirs[dir], amount)
        if turn is not None:
            dir = rotate(dir, turn)

    return (pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + dir


class Faces(Enum):
    FRONT = 0
    RIGHT = 1
    BACK = 2
    LEFT = 3
    TOP = 4
    BOTTOM = 5


def wrap(
    map_size: int,
    pos: Tuple[int, int, Faces],
    dir: Tuple[int, int],
) -> Tuple[Tuple[int, int, Faces], Tuple[int, int]]:
    dir_x, dir_y = dir
    x, y, z = pos
    max_x, max_y = map_size - 1, map_size - 1
    if dir_x != 0:
        assert dir_y == 0
        if x < 0:
            assert dir_x == -1
            if z == Faces.TOP:
                return (y, 0, Faces.LEFT), (0, 1)
            elif z == Faces.BOTTOM:
                return (max_x - y, max_y, Faces.LEFT), (0, -1)
            else:
                return (max_x, y, Faces((z.value - 1) % 4)), dir
        elif x > max_x:
            assert dir_x == 1
            if z == Faces.TOP:
                return (max_x - y, 0, Faces.RIGHT), (0, 1)
            elif z == Faces.BOTTOM:
                return (y, max_y, Faces.RIGHT), (0, -1)
            else:
                return (0, y, Faces((z.value + 1) % 4)), dir
    else:
        assert dir_y != 0
        if y < 0:
            assert dir_y == -1
            if z == Faces.TOP:
                return (max_x - x, 0, Faces.BACK), (0, 1)
            elif z == Faces.BOTTOM:
                return (x, max_y, Faces.FRONT), dir
            elif z == Faces.FRONT:
                return (x, max_y, Faces.TOP), dir
            elif z == Faces.BACK:
                return (max_x - x, 0, Faces.TOP), (0, 1)
            elif z == Faces.LEFT:
                return (0, x, Faces.TOP), (1, 0)
            else:
                assert z == Faces.RIGHT
                return (max_x, max_y - x, Faces.TOP), (-1, 0)
        elif y > max_y:
            assert dir_y == 1
            if z == Faces.TOP:
                return (x, 0, Faces.FRONT), dir
            elif z == Faces.BOTTOM:
                return (max_x - x, max_y, Faces.BACK), (0, -1)
            elif z == Faces.FRONT:
                return (x, 0, Faces.BOTTOM), dir
            elif z == Faces.BACK:
                return (max_x - x, max_y, Faces.BOTTOM), (0, -1)
            elif z == Faces.LEFT:
                return (0, max_y - x, Faces.BOTTOM), (1, 0)
            else:
                assert z == Faces.RIGHT
                return (max_x, x, Faces.BOTTOM), (-1, 0)
    return pos, dir


def print_map(maps: List[np.ndarray], pos: Tuple[int, int, Faces], dir: int):
    print(pos[2], ":")
    map = maps[pos[2].value]
    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            if x == pos[0] and y == pos[1]:
                print(">v<^"[dir], end="")
            else:
                print(map[y, x], end="")

        print()


def move2(
    maps: Dict[Faces, np.ndarray],
    dirs: List[Tuple[int, int]],
    pos: Tuple[int, int, Faces],
    dir_idx: int,
    amount: int,
) -> Tuple[Tuple[int, int, Faces], int]:
    last_ok_pos = pos
    dir = dirs[dir_idx]

    while amount > 0:
        # print_map(maps, pos, dirs.index(dir))

        new_pos = pos[0] + dir[0], pos[1] + dir[1], pos[2]

        new_pos, new_dir = wrap(maps[pos[2]].shape[0], new_pos, dir)
        try:
            char = maps[new_pos[2]][new_pos[1], new_pos[0]]
        except:
            print(maps[new_pos[2]].shape)
            print(pos, new_pos, dir, new_dir)
            raise
        if char == "#":
            break
        elif char == ".":
            amount -= 1
            last_ok_pos = new_pos
        else:
            print(pos, new_pos)
            raise RuntimeError
        pos = new_pos
        dir = new_dir

    return last_ok_pos, dirs.index(dir)


part2_test_input = part1_test_input

part2_test_output = 5031

IS_TEST: bool


def part2(inp: TextIOWrapper):
    map, path = inp.read().split("\n\n")
    map = [list(r) for r in map.split("\n")]
    max_w = max(len(r) for r in map)
    map = [xi + [" "] * (max_w - len(xi)) for xi in map]
    map_img = np.array(map)
    print(map_img)
    maps: Dict[Faces, np.ndarray] = {}
    transform: Dict[Faces, Tuple[Tuple[int, int], int]] = {}
    if IS_TEST:
        w = 4
        transform[Faces.FRONT] = ((2, 0), 0)
        transform[Faces.RIGHT] = ((3, 2), 2)
        transform[Faces.BACK] = ((2, 2), 2)
        transform[Faces.LEFT] = ((1, 1), -1)
        transform[Faces.TOP] = ((0, 1), 2)
        transform[Faces.BOTTOM] = ((2, 1), 0)
    else:
        w = 50
        transform[Faces.FRONT] = ((1, 0), 0)
        transform[Faces.RIGHT] = ((2, 0), 0)
        transform[Faces.BACK] = ((1, 2), 2)
        transform[Faces.LEFT] = ((0, 2), 2)
        transform[Faces.TOP] = ((0, 3), 1)  # ???
        transform[Faces.BOTTOM] = ((1, 1), 0)

    for face, ((tx, ty), rot) in transform.items():
        maps[face] = np.rot90(
            map_img[ty * w : (ty + 1) * w, tx * w : (tx + 1) * w], rot
        )

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dir = 0

    pos = (0, 0, Faces.FRONT)

    for m in re.finditer("(\d+)([LR])?", path):
        amount, turn = m.groups()
        amount = int(amount)

        pos, dir = move2(maps, dirs, pos, dir, amount)
        if turn is not None:
            dir = rotate(dir, turn)

    print("Position", pos, "Direction", dir)
    x, y = pos[:2]
    (tx, ty), rot = transform[pos[2]]
    if rot == 2:
        x = w - 1 - x
        y = w - 1 - y
        dir = (dir + 2) % 4
    elif rot == -1:
        x, y = y, w - 1 - x
        dir = (dir - 1) % 4
    else:
        assert rot == 0

    print("Position", (x, y), "Direction", dir)
    x += tx * w
    y += ty * w
    print("Position", (x, y), "Direction", dir)

    return (y + 1) * 1000 + (x + 1) * 4 + dir
