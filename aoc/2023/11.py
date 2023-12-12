from io import StringIO, TextIOWrapper
import itertools
import sys

part1_test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    lines = [list(l.strip()) for l in inp.readlines()]

    empty_columns = set()
    for x in range(len(lines[0])):
        if all([lines[y][x] == "." for y in range(len(lines))]):
            empty_columns.add(x)

    add_y = 0
    galaxies = list()
    for y, l in enumerate(lines):
        if all([l[x] == "." for x in range(len(l))]):
            add_y += 1
            continue
        add_x = 0
        for x, c in enumerate(l):
            if x in empty_columns:
                add_x += 1
            elif c == "#":
                galaxies.append((x + add_x, y + add_y))

    answer = 0
    for (x1, y1), (x2, y2) in itertools.combinations(galaxies, 2):
        answer += abs(x1 - x2) + abs(y1 - y2)

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    lines = [list(l.strip()) for l in inp.readlines()]

    empty_columns = set()
    for x in range(len(lines[0])):
        if all([lines[y][x] == "." for y in range(len(lines))]):
            empty_columns.add(x)

    add_y = 0
    galaxies = list()
    for y, l in enumerate(lines):
        if all([l[x] == "." for x in range(len(l))]):
            add_y += 1_000_000 - 1
            continue
        add_x = 0
        for x, c in enumerate(l):
            if x in empty_columns:
                add_x += 1_000_000 - 1
            elif c == "#":
                galaxies.append((x + add_x, y + add_y))

    answer = 0
    for (x1, y1), (x2, y2) in itertools.combinations(galaxies, 2):
        answer += abs(x1 - x2) + abs(y1 - y2)

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
