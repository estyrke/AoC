from io import StringIO, TextIOBase
import sys


part1_test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

part1_test_output = 2
IS_TEST = False


def dfs(map, start, goal, visited: set[tuple[int, int]] | None = None):
    stack = [(start, [start])]

    if visited is None:
        visited = set()
    while stack:
        (x, y), path = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if map[new_y][new_x] == "#":
                continue
            if (new_x, new_y) in path:
                continue
            new_path = path + [(new_x, new_y)]
            if (new_x, new_y) == goal:
                return new_path
            stack.append(((new_x, new_y), new_path))
    return None


def part1(inp: TextIOBase):
    if IS_TEST:
        threshold = 39
    else:
        threshold = 100

    orig_map = [list(line.strip()) for line in inp]

    for y, row in enumerate(orig_map):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)

    path = dfs(orig_map, start, end)
    assert path
    path = {pos: i for i, pos in enumerate(path)}
    answer = 0
    for (cheat_start_x, cheat_start_y), cheat_dist in path.items():
        for dx1, dy1 in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if orig_map[cheat_start_y + dy1][cheat_start_x + dx1] != "#":
                continue

            for dx2, dy2 in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                if dx1 + dx2 == 0 and dy1 + dy2 == 0:
                    continue
                cheat_end_dist = path.get((cheat_start_x + dx1 + dx2, cheat_start_y + dy1 + dy2))
                if cheat_end_dist is None:
                    continue
                cheat_save_steps = cheat_end_dist - cheat_dist - 2
                if cheat_save_steps <= 0:
                    continue
                if cheat_save_steps >= threshold:
                    answer += 1
    return answer


part2_test_input = part1_test_input

part2_test_output = 29


def part2(inp: TextIOBase):
    if IS_TEST:
        threshold = 71
    else:
        threshold = 100

    orig_map = [list(line.strip()) for line in inp]

    for y, row in enumerate(orig_map):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)

    path = dfs(orig_map, start, end)
    assert path
    answer = 0
    print(f"path is {len(path)-1} ps long")
    for cheat_dist, (cheat_start_x, cheat_start_y) in enumerate(path):
        for cheat_save_offset, (cheat_end_x, cheat_end_y) in enumerate(path[cheat_dist + threshold :]):
            cheat_steps = abs(cheat_end_x - cheat_start_x) + abs(cheat_end_y - cheat_start_y)
            cheat_save_steps = cheat_save_offset + threshold - cheat_steps

            if cheat_steps > 20:
                continue

            if cheat_save_steps >= threshold:
                answer += 1
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
