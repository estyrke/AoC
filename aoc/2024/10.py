from io import StringIO, TextIOBase
import sys

part1_test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

part1_test_output = 36


def part1(inp: TextIOBase):
    answer = None

    grid = [[int(c) for c in l.strip()] for l in inp.readlines()]

    trailheads = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                trailheads.append((y, x))

    answer = 0
    for th in trailheads:
        queue = [(0, th)]
        visited = set()
        while queue:
            height, pos = queue.pop(0)
            y, x = pos
            if pos in visited:
                continue
            visited.add(pos)
            if grid[y][x] == 9:
                answer += 1
                continue
            for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == grid[y][x] + 1:
                    queue.append((height + 1, (ny, nx)))
        print(answer)
    return answer


part2_test_input = part1_test_input

part2_test_output = 81


def part2(inp: TextIOBase):
    grid = [[int(c) for c in l.strip()] for l in inp.readlines()]

    trailheads = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                trailheads.append((y, x))

    answer = 0
    for th in trailheads:
        queue = [(0, th, "")]  # height, pos, path
        visited = set()
        rating = 0
        while queue:
            height, pos, path = queue.pop(0)
            y, x = pos

            visited.add(path)
            if grid[y][x] == 9:
                rating += 1
                continue
            for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == grid[y][x] + 1:
                    new_path = path + f"({ny},{nx})"
                    if new_path not in visited:
                        queue.append((height + 1, (ny, nx), new_path))
        print(rating)
        answer += rating
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
