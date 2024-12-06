from io import StringIO, TextIOBase
import sys

part1_test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

part1_test_output = 41


def part1(inp: TextIOBase):
    answer = 0

    grid = [list(l.strip()) for l in inp.readlines()]

    pos = 0, 0
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "^":
                pos = (x, y)

    # print(pos)
    x, y = pos
    dx, dy = 0, -1
    while x < len(grid[0]) and y < len(grid) and x >= 0 and y >= 0:
        if grid[y][x] in [".", "^"]:
            answer += 1
            grid[y][x] = "X"
        elif grid[y][x] == "#":
            y -= dy
            x -= dx
            dx, dy = -dy, dx

        x += dx
        y += dy
    # print("\n".join("".join(line) for line in grid))
    return answer


part2_test_input = part1_test_input

part2_test_output = 6


def part2(inp: TextIOBase):
    answer = 0

    grid = [list(l.strip()) for l in inp.readlines()]

    start_pos: tuple[int, int] = 0, 0
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "^":
                start_pos = (x, y)

    print(start_pos)
    x, y = start_pos
    dx, dy = 0, -1
    candidates: set[tuple[int, int, int, int]] = set()
    travel(grid, y, x, dx, dy, candidates)
    tried = {start_pos}
    positions = []
    while candidates:
        ox, oy, _, _ = candidates.pop()
        if (ox, oy) in tried:
            continue
        tried.add((ox, oy))
        grid[oy][ox] = "#"
        if travel(grid, y, x, dx, dy):
            answer += 1
            positions.append((x, y))
        grid[oy][ox] = "."

    for x, y in positions:
        grid[y][x] = "O"
    # print("\n".join("".join(line) for line in grid))

    assert answer != 2225
    return answer


def travel(grid, y, x, dx, dy, visited: set[tuple[int, int, int, int]] | None = None):
    if visited is None:
        visited = set()
    while x < len(grid[0]) and y < len(grid) and x >= 0 and y >= 0:
        if grid[y][x] in [".", "^"]:
            if (x, y, dx, dy) in visited:
                return 1
            visited.add((x, y, dx, dy))
        elif grid[y][x] == "#":
            y -= dy
            x -= dx
            dx, dy = -dy, dx

        x += dx
        y += dy
    return 0


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
