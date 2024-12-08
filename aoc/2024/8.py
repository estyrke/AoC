from collections import defaultdict
from io import StringIO, TextIOBase
import itertools
import sys

part1_test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

part1_test_output = 14


def part1(inp: TextIOBase):
    answer = None

    grid = [list(l.strip()) for l in inp.readlines()]

    frequencies = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                frequencies[cell].append((y, x))

    antinodes: set[tuple[int, int]] = set()
    for freq, coords in frequencies.items():
        for pair in itertools.combinations(coords, 2):
            y1, x1 = pair[0]
            y2, x2 = pair[1]
            a1 = (y1 + (y2 - y1) * 2, x1 + (x2 - x1) * 2)
            a2 = (y2 + (y1 - y2) * 2, x2 + (x1 - x2) * 2)
            antinodes.add(a1)
            antinodes.add(a2)
    answer = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in antinodes:
                print("X", end="")
                answer += 1
            else:
                print(cell, end="")
        print()
    return answer


part2_test_input = part1_test_input

part2_test_output = 34


def part2(inp: TextIOBase):
    grid = [list(l.strip()) for l in inp.readlines()]

    frequencies = defaultdict(list)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                frequencies[cell].append((y, x))

    antinodes: set[tuple[int, int]] = set()
    for freq, coords in frequencies.items():
        for pair in itertools.combinations(coords, 2):
            y1, x1 = pair[0]
            y2, x2 = pair[1]

            dx, dy = x2 - x1, y2 - y1
            while True:
                antinodes.add((y1, x1))
                antinodes.add((y2, x2))
                x1 += dx
                y1 += dy
                x2 -= dx
                y2 -= dy
                if (x1 < 0 or x1 >= len(grid[0]) or y1 < 0 or y1 >= len(grid)) and (
                    x2 < 0 or x2 >= len(grid[0]) or y2 < 0 or y2 >= len(grid)
                ):
                    break
    answer = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) in antinodes:
                print("X", end="")
                answer += 1
            else:
                print(cell, end="")
        print()
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
