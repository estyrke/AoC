from io import TextIOWrapper
import math

test_input = """.#.
..#
###"""
test_output = 848


def neighbors(cubes: set, x: int, y: int, z: int, w: int) -> int:
    n = 0

    for dw in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (x+dx, y+dy, z+dz, w+dw) in cubes:
                        n+= 1

    if (x, y, z, w) in cubes:
        n -= 1
    return n

def iterate(cubes: set) -> set:
    min_w = min([c[3] for c in cubes])
    max_w = max([c[3] for c in cubes])

    min_z = min([c[2] for c in cubes])
    max_z = max([c[2] for c in cubes])
    min_y = min([c[1] for c in cubes])
    max_y = max([c[1] for c in cubes])
    min_x = min([c[0] for c in cubes])
    max_x = max([c[0] for c in cubes])

    new_cubes = set()
    for w in range(min_w - 1, max_w + 2):
        for z in range(min_z - 1, max_z + 2):
            for y in range(min_y - 1, max_y + 2):
                for x in range(min_x - 1, max_x + 2):
                    n = neighbors(cubes, x, y, z, w)
                    if (x, y, z, w) in cubes:
                        if 2 <= n <= 3:
                            new_cubes.add((x, y, z, w))
                    else:
                        if n == 3:
                            new_cubes.add((x, y, z, w))

    return new_cubes

def solve(inp: TextIOWrapper):
    answer = 2

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]
    cubes = {
        (x, y, 0, 0) for y, l in enumerate(lines) for x, c in enumerate(l) if c == "#"
    }

    for cycle in range(6):
        cubes = iterate(cubes)
    return len(cubes)
