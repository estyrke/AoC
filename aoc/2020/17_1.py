from io import TextIOWrapper
import math

test_input = """.#.
..#
###"""
test_output = 112


def neighbors(cubes: set, x: int, y: int, z: int) -> int:
    n = 0

    if (x-1, y-1, z-1) in cubes: n+= 1
    if (x-1, y-1, z) in cubes: n+= 1
    if (x-1, y-1, z+1) in cubes: n+= 1
    if (x-1, y, z-1) in cubes: n+= 1
    if (x-1, y, z) in cubes: n+= 1
    if (x-1, y, z+1) in cubes: n+= 1
    if (x-1, y+1, z-1) in cubes: n+= 1
    if (x-1, y+1, z) in cubes: n+= 1
    if (x-1, y+1, z+1) in cubes: n+= 1

    if (x, y-1, z-1) in cubes: n+= 1
    if (x, y-1, z) in cubes: n+= 1
    if (x, y-1, z+1) in cubes: n+= 1
    if (x, y, z-1) in cubes: n+= 1
    if (x, y, z+1) in cubes: n+= 1
    if (x, y+1, z-1) in cubes: n+= 1
    if (x, y+1, z) in cubes: n+= 1
    if (x, y+1, z+1) in cubes: n+= 1

    if (x+1, y-1, z-1) in cubes: n+= 1
    if (x+1, y-1, z) in cubes: n+= 1
    if (x+1, y-1, z+1) in cubes: n+= 1
    if (x+1, y, z-1) in cubes: n+= 1
    if (x+1, y, z) in cubes: n+= 1
    if (x+1, y, z+1) in cubes: n+= 1
    if (x+1, y+1, z-1) in cubes: n+= 1
    if (x+1, y+1, z) in cubes: n+= 1
    if (x+1, y+1, z+1) in cubes: n+= 1

    return n

def iterate(cubes: set) -> set:
    min_z = min([c[2] for c in cubes])
    max_z = max([c[2] for c in cubes])
    min_y = min([c[1] for c in cubes])
    max_y = max([c[1] for c in cubes])
    min_x = min([c[0] for c in cubes])
    max_x = max([c[0] for c in cubes])

    new_cubes = set()
    for z in range(min_z - 1, max_z + 2):
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                n = neighbors(cubes, x, y, z)
                if (x, y, z) in cubes:
                    if 2 <= n <= 3:
                        new_cubes.add((x, y, z))
                else:
                    if n == 3:
                        new_cubes.add((x, y, z))

    return new_cubes

def solve(inp: TextIOWrapper):
    answer = 2

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]
    cubes = {
        (x, y, 0) for y, l in enumerate(lines) for x, c in enumerate(l) if c == "#"
    }

    min_x, max_x = 0, len(lines[0])
    for cycle in range(6):
        print(cubes)
        cubes = iterate(cubes)
    return len(cubes)
