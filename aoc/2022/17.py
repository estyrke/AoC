from collections import defaultdict
from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

part1_test_output = 3068


class Shape:
    def __init__(self, grid: list, profile):
        self.shape = list(reversed(grid))
        self.h = len(grid)
        self.w = len(grid[0])
        self.profile = profile

    def collides(self, field, height, pos):
        for ri, r in enumerate(self.shape):
            field_row = height + ri
            if len(field) <= field_row:
                continue
            for ci, c in enumerate(r):
                if c == ".":
                    continue
                if field[field_row][pos + ci] != ".":
                    return True
        return False


shapes = [
    Shape(["####"], [1, 1, 1, 1]),
    Shape([".#.", "###", ".#."], [2, 3, 2]),
    Shape(["..#", "..#", "###"], [1, 1, 3]),
    Shape(["#", "#", "#", "#"], [4]),
    Shape(["##", "##"], [2, 2]),
]


def part1(inp: TextIOWrapper):
    moves = [1 if c == ">" else -1 for c in inp.read().strip()]
    answer = simulate(moves, 2022)

    return answer


part2_test_input = part1_test_input

part2_test_output = 1514285714288


def part2(inp: TextIOWrapper):
    moves = [1 if c == ">" else -1 for c in inp.read().strip()]

    blocks = 1_000_000_000_000

    return simulate(moves, blocks)


def simulate(moves: list, blocks: int):
    field = [list("#######")]
    jet_pos = 0
    dist = defaultdict(int)
    dist_jet = defaultdict(int)
    jet_sync = dict()
    jet_cycle = dict()
    jet_height = dict()
    init_heights = dict()
    cycle = None

    for i in range(blocks):
        if i > 0 and jet_pos == 0:
            print(i, i % len(shapes))
            if i % len(shapes) == 0:
                return i
        assert "#" in field[-1]
        # print("\n".join(["".join(x) for x in field]), "\n")
        shape = shapes[i % len(shapes)]
        pos = 2
        height = len(field) + 3

        collide = False
        falling = 0
        while not collide:

            # print(height, pos, jet_pos, moves[jet_pos])
            pos += moves[jet_pos]

            if pos < 0:
                pos += 1
            elif pos + shape.w > 7:
                pos -= 1
            elif falling >= 3 and shape.collides(field, height, pos):
                pos -= moves[jet_pos]

            jet_pos = (jet_pos + 1) % len(moves)

            height -= 1
            collide = falling >= 3 and shape.collides(field, height, pos)
            falling += 1

        if cycle is None:
            init_heights[i] = len(field)
        dist_jet[jet_pos] += 1
        if dist_jet[jet_pos] > 2 and i % len(shapes) == jet_sync[jet_pos]:
            height_increase = len(field) - jet_height[jet_pos]
            cycle = i - jet_cycle[jet_pos]
            mul, mod = divmod(blocks, cycle)
            # print(i, total_jet, jet_pos, dist_jet[jet_pos], i % len(shapes), jet_sync[jet_pos], cycle, height_increase)
            if i % mod == 0:
                assert init_heights[mod] > 0
                return height_increase * mul + init_heights[mod] - 1

        jet_height[jet_pos] = len(field)
        jet_sync[jet_pos] = i % len(shapes)
        jet_cycle[jet_pos] = i
        dist[falling] += 1
        height += 1
        for y in range(height, height + shape.h):
            if y >= len(field):
                field.append(["."] * 7)
            for x in range(pos, pos + shape.w):
                assert x >= 0
                assert x < 7
                if shape.shape[y - height][x - pos] == "#":
                    field[y][x] = "#"

    return len(field) - 1
