from io import StringIO, TextIOBase
import sys

part1_test_input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

part1_test_output = 11048


def part1(inp: TextIOBase):
    answer = None

    map = [list(l.strip()) for l in inp.readlines()]

    start: tuple[int, int] = (0, 0)
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
                break
    facing: tuple[int, int] = (1, 0)

    def neighbors(pos):
        x, y = pos
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if map[ny][nx] != "#":
                yield (nx, ny)

    queue: list[tuple[tuple[int, int], int, tuple[int, int]]] = [(start, 0, facing)]
    visited = {}
    while queue:
        pos, score, facing = queue.pop(0)
        x, y = pos
        if pos in visited and visited[pos] <= score:
            continue
        visited[(pos)] = score

        if map[pos[1]][pos[0]] == "E":
            answer = min(answer, score) if answer is not None else score
            continue

        for n_x, n_y in neighbors(pos):
            # if npos in path:
            #    continue
            new_facing = (n_x - x, n_y - y)
            if new_facing == facing:
                new_score = score + 1
            else:
                new_score = score + 1000 + 1

            queue.append(((n_x, n_y), new_score, new_facing))

    assert answer is not None
    return answer


part2_test_input = part1_test_input

part2_test_output = 64


def part2(inp: TextIOBase):
    input = inp.read()
    map = [list(l.strip()) for l in input.splitlines()]

    start: tuple[int, int] = (0, 0)
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
                break
    facing: tuple[int, int] = (1, 0)

    def neighbors(pos):
        x, y = pos
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if map[ny][nx] != "#":
                yield (nx, ny)

    queue: list[tuple[tuple[int, int], int, set[tuple[int, int]], tuple[int, int]]] = [(start, 0, set([start]), facing)]
    visited = {}
    best_score = part1(StringIO(input))
    best_spots = set()
    while queue:
        pos, score, path, facing = queue.pop(0)
        x, y = pos
        if score > best_score:
            continue

        if (pos, facing) in visited and visited[(pos, facing)] < score:
            continue
        visited[(pos, facing)] = score

        if map[pos[1]][pos[0]] == "E":
            if score == best_score:
                for pos in path:
                    best_spots.add(pos)
            continue

        for n_x, n_y in neighbors(pos):
            # if npos in path:
            #    continue
            new_facing = (n_x - x, n_y - y)
            if (n_x, n_y) in path:
                # 180 turn, skip
                continue
            elif new_facing == facing:
                new_score = score + 1
            else:
                new_score = score + 1000 + 1
            if new_score > best_score:
                continue
            queue.append(((n_x, n_y), new_score, path | set([(n_x, n_y)]), new_facing))

    return len(best_spots)


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
