from io import TextIOWrapper
import math
import functools
import itertools
from queue import PriorityQueue
from typing import Optional, Tuple
from ..tools import parse_input

part1_test_input = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

part1_test_output = 18


def dist(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def part1(inp: TextIOWrapper):
    maze = [list(l.strip()[1:-1]) for l in inp.readlines()]
    maze = maze[1:-1]
    blizzards = set()
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == ">":
                blizzards.add((x, y, (1, 0)))
            elif c == "<":
                blizzards.add((x, y, (-1, 0)))
            elif c == "^":
                blizzards.add((x, y, (0, -1)))
            elif c == "v":
                blizzards.add((x, y, (0, 1)))
            else:
                assert c == "." or c == "#"

    height = len(maze)
    width = len(maze[0])

    confs = [blizzards]
    print("Cycle is", width * height // math.gcd(width, height))
    for i in range(width * height // math.gcd(width, height) - 1):
        blizzards = {
            ((x + dx) % width, (y + dy) % height, (dx, dy))
            for x, y, (dx, dy) in blizzards
        }
        confs.append({(x, y) for x, y, _ in blizzards})

    blizzards2 = {
        ((x + dx) % width, (y + dy) % height, (dx, dy)) for x, y, (dx, dy) in blizzards
    }

    assert confs[0] == blizzards2

    start = (0, -1)
    goal = (width - 1, height - 1)

    return walk(start, 0, goal, confs, width, height)


def walk(start, start_z, goal, confs, width, height) -> Optional[int]:
    queue = PriorityQueue()
    queue.put((dist(start, goal), start, start_z))
    visited = set()
    while not queue.empty():
        _d, pos, z = queue.get()
        if pos == goal:
            return z + 1
        neighbors = [
            ((pos[0] + 1, pos[1]), z + 1),
            ((pos[0] - 1, pos[1]), z + 1),
            ((pos[0], pos[1] + 1), z + 1),
            ((pos[0], pos[1] - 1), z + 1),
            (pos, z + 1),  # Stay in place
        ]

        neighbors = [
            ((new_x, new_y), new_z)
            for (new_x, new_y), new_z in neighbors
            if new_x >= 0
            and new_x < width
            and (new_y >= 0 or (new_x, new_y) == start)
            and (new_y < height or (new_x, new_y) == start)
            and (new_x, new_y) not in confs[(new_z) % len(confs)]
        ]

        for new_pos, new_z in neighbors:
            if (new_pos, new_z % len(confs)) not in visited:
                visited.add((new_pos, new_z % len(confs)))
                queue.put((dist(new_pos, goal) + new_z, new_pos, new_z))


part2_test_input = part1_test_input

part2_test_output = 54


def part2(inp: TextIOWrapper):
    maze = [list(l.strip()[1:-1]) for l in inp.readlines()]
    maze = maze[1:-1]
    blizzards = set()
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == ">":
                blizzards.add((x, y, (1, 0)))
            elif c == "<":
                blizzards.add((x, y, (-1, 0)))
            elif c == "^":
                blizzards.add((x, y, (0, -1)))
            elif c == "v":
                blizzards.add((x, y, (0, 1)))
            else:
                assert c == "." or c == "#"

    height = len(maze)
    width = len(maze[0])

    confs = [blizzards]
    print("Cycle is", width * height // math.gcd(width, height))
    for i in range(width * height // math.gcd(width, height) - 1):
        blizzards = {
            ((x + dx) % width, (y + dy) % height, (dx, dy))
            for x, y, (dx, dy) in blizzards
        }
        confs.append({(x, y) for x, y, _ in blizzards})

    blizzards2 = {
        ((x + dx) % width, (y + dy) % height, (dx, dy)) for x, y, (dx, dy) in blizzards
    }

    assert confs[0] == blizzards2

    start = (0, -1)
    goal = (width - 1, height - 1)

    l1 = walk(start, 0, goal, confs, width, height)
    print(l1)
    l2 = walk((width - 1, height), l1, (0, 0), confs, width, height)
    print(l2)
    l3 = walk(start, l2, goal, confs, width, height)
    print(l3)
    return l3
