from io import TextIOWrapper
import math


def solve(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]
    cubes = {
        (x, y, 0) for y, l in enumerate(lines) for x, c in enumerate(l) if c == "#"
    }

    min_x, max_x = 0, len(lines[0])
    for cycle in range(6):
        min_x = min([c[0] for c in cubes])
        max_x = max([c[0] for c in cubes])
    return answer
