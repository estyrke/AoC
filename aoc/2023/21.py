from functools import lru_cache
from io import StringIO, TextIOWrapper
import sys

part1_test_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

part1_test_output = 16


@lru_cache
def neigh(pos: tuple[int, int]):
    x, y = pos
    return [
        (x + dx, y + dy)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if 0 <= x + dx < len(lines[0])
        and 0 <= y + dy < len(lines)
        and lines[y + dy][x + dx] != "#"
    ]


def part1(inp: TextIOWrapper):
    global lines

    # for line in inp.readlines():
    lines = [l.strip() for l in inp.readlines()]

    if len(lines) == 11:
        # Test mode
        steps = 6
    else:
        # Real input
        steps = 64

    start = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                start = (x, y)
    assert start is not None

    queue: list[tuple[tuple[int, int], int]] = [(start, steps)]
    reachable = set()
    visited = {start: steps}

    while queue:
        next, dist = queue.pop(0)
        if dist > 0:
            for n in neigh(next):
                if n not in visited:
                    visited[n] = dist - 1
                    queue.append((n, dist - 1))

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if (x, y) in visited:
                # print(f"{visited[(x, y)]:02}", end="")
                if visited[(x, y)] % 2 == 0:
                    reachable.add((x, y))
            # else:
            #    print(f" {c}", end="")
        # print()
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return len(reachable)


part2_test_input = None  # part1_test_input

part2_test_output = None  # 16733044


def part2(inp: TextIOWrapper):
    global lines

    lines = [l.strip() for l in inp.readlines()]

    start = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                start = (x, y)
    assert start is not None

    size = len(lines)
    dup = 5
    lines = [l * dup for l in lines]
    lines = lines * dup
    start = (start[0] + size * (dup // 2), start[1] + size * (dup // 2))

    r = []
    neigh.cache_clear()

    for steps in [65, 65 + 131, 65 + 131 * 2]:
        queue: list[tuple[tuple[int, int], int]] = [(start, steps)]
        visited = {start: steps}

        while queue:
            next, dist = queue.pop(0)
            if dist > 0:
                for n in neigh(next):
                    if n not in visited:
                        visited[n] = dist - 1
                        queue.append((n, dist - 1))

        reachable = set()
        for y, l in enumerate(lines):
            for x, c in enumerate(l):
                if (x, y) in visited:
                    if visited[(x, y)] % 2 == 0:
                        reachable.add((x, y))
        r.append(len(reachable))

    # print(r)
    d1 = [b - a for a, b in zip(r, r[1:])]
    # print(d1)
    d2 = [b - a for a, b in zip(d1, d1[1:])]
    # print(d2)

    blocks, rest = divmod(26501365 - 65, 131)
    # print(blocks, rest)
    assert rest == 0

    # quadratic formula: a*x**2 + b*x + c
    c = r[0]
    a = d2[0] // 2
    b = d1[0] - a

    answer = a * blocks * blocks + b * blocks + c
    assert answer < 1214656602936000
    assert answer < 607334338912829
    assert answer > 81850580000

    return answer


def print_map(visited: dict[tuple[int, int], int]):
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if (x, y) in visited:
                print(f"{visited[(x, y)]:3}", end="")
            else:
                print(f" {c} ", end="")
        print()
    print()


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
