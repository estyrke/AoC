from io import StringIO, TextIOBase
import sys

part1_test_input = """....#
#..#.
#..##
..#..
#...."""

part1_test_output = 2129920


def part1(inp: TextIOBase):
    answer = None

    map = [list(line.strip()) for line in inp]
    seen = set()
    while True:
        bio = sum(2 ** (y * 5 + x) for y, row in enumerate(map) for x, cell in enumerate(row) if cell == "#")
        if bio in seen:
            answer = bio
            break
        seen.add(bio)
        new_map = [row.copy() for row in map]
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                neighbors = 0
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 5 and 0 <= ny < 5:
                        if map[ny][nx] == "#":
                            neighbors += 1
                if cell == "#" and neighbors != 1:
                    new_map[y][x] = "."
                if cell == "." and neighbors in (1, 2):
                    new_map[y][x] = "#"
        map = new_map

    return answer


part2_test_input = part1_test_input

part2_test_output = 99


def part2(inp: TextIOBase):
    answer = None

    map = [list(line.strip()) for line in inp]
    levels = {0: map}

    assert list(neighbors(3, 3, 0)) == [
        (3, 4, 0),
        (3, 2, 0),
        (4, 3, 0),
        (2, 3, 0),
    ], list(neighbors(3, 3, 0))
    assert list(neighbors(1, 1, 0)) == [
        (1, 2, 0),
        (1, 0, 0),
        (2, 1, 0),
        (0, 1, 0),
    ], list(neighbors(1, 1, 0))
    assert list(neighbors(3, 0, 0)) == [
        (2, 1, -1),
        (3, 1, 0),
        (4, 0, 0),
        (2, 0, 0),
    ], list(neighbors(3, 0, 0))
    assert list(neighbors(4, 0, 0)) == [
        (3, 2, -1),
        (2, 1, -1),
        (4, 1, 0),
        (3, 0, 0),
    ], list(neighbors(4, 0, 0))
    if IS_TEST:
        total_minutes = 10
    else:
        total_minutes = 200
    for minute in range(total_minutes):
        new_levels = {}
        min_level = min(levels.keys())
        max_level = max(levels.keys())
        levels[min_level - 1] = [["."] * 5 for _ in range(5)]
        levels[max_level + 1] = [["."] * 5 for _ in range(5)]
        for level, map in levels.items():
            new_map = [row.copy() for row in map]
            for y, row in enumerate(map):
                for x, cell in enumerate(row):
                    if x == 2 and y == 2:
                        continue
                    adj = 0
                    for nx, ny, nz in neighbors(x, y, level):
                        if nz in levels and levels[nz][ny][nx] == "#":
                            adj += 1
                    if cell == "#" and adj != 1:
                        new_map[y][x] = "."
                    if cell == "." and adj in (1, 2):
                        new_map[y][x] = "#"
            new_levels[level] = new_map
        levels = new_levels

    answer = 0
    for level, map in levels.items():
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                if cell == "#":
                    answer += 1
    return answer


def neighbors(x: int, y: int, level: int):
    if x == 0:
        yield 1, 2, level - 1
    if x == 4:
        yield 3, 2, level - 1
    if y == 0:
        yield 2, 1, level - 1
    if y == 4:
        yield 2, 3, level - 1
    if x == 1 and y == 2:
        for ny in range(5):
            yield 0, ny, level + 1
    if x == 3 and y == 2:
        for ny in range(5):
            yield 4, ny, level + 1
    if x == 2 and y == 1:
        for nx in range(5):
            yield nx, 0, level + 1
    if x == 2 and y == 3:
        for nx in range(5):
            yield nx, 4, level + 1

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if nx == 2 and ny == 2:
            continue
        if 0 <= nx < 5 and 0 <= ny < 5:
            yield nx, ny, level


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
