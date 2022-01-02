from io import TextIOWrapper
import math
from typing import Dict, Tuple

from .intcode import Machine


part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    m = Machine.from_str(inp.read())

    result: Dict[Tuple[int, int], int] = {}
    coord = 0, 0
    dir = 0
    painted = 0
    while not m.halted:
        color = result.get(coord, 0)
        out = m.run([color])

        assert len(out) == 2
        new_color, turn = out

        if coord not in result:
            painted += 1

        result[coord] = new_color
        if turn == 0:
            dir = (dir - 1) % 4
        else:
            assert turn == 1
            dir = (dir + 1) % 4

        if dir == 0:
            coord = coord[0], coord[1] - 1
        elif dir == 1:
            coord = coord[0] + 1, coord[1]
        elif dir == 2:
            coord = coord[0], coord[1] + 1
        else:
            assert dir == 3
            coord = coord[0] - 1, coord[1]

    return painted


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    m = Machine.from_str(inp.read())

    result: Dict[Tuple[int, int], int] = {(0, 0): 1}
    coord = 0, 0
    dir = 0
    painted = 0
    while not m.halted:
        color = result.get(coord, 0)
        out = m.run([color])

        assert len(out) == 2
        new_color, turn = out

        if coord not in result:
            painted += 1

        result[coord] = new_color
        if turn == 0:
            dir = (dir - 1) % 4
        else:
            assert turn == 1
            dir = (dir + 1) % 4

        if dir == 0:
            coord = coord[0], coord[1] - 1
        elif dir == 1:
            coord = coord[0] + 1, coord[1]
        elif dir == 2:
            coord = coord[0], coord[1] + 1
        else:
            assert dir == 3
            coord = coord[0] - 1, coord[1]

    for y in range(6):
        for x in range(50):
            if result.get((x, y), 0) == 1:
                print("#", end="")
            else:
                print(" ", end="")

        print()
