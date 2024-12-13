from collections import defaultdict
from io import StringIO, TextIOBase
from pprint import pprint
import sys


part1_test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

part1_test_output = 1930


def part1(inp: TextIOBase):
    answer = 0

    map = [list(x.strip()) for x in inp.read().strip().splitlines()]
    visited = [[False for _ in range(len(map[0]))] for _ in range(len(map))]

    for y in range(len(map)):
        for x in range(len(map[0])):
            if visited[y][x]:
                continue

            type = map[y][x]
            queue = [(y, x)]
            visited[y][x] = True
            perimeter = 0
            area = 0
            while queue:
                y2, x2 = queue.pop(0)
                border = 4
                for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    ny, nx = y2 + dy, x2 + dx
                    if 0 <= ny < len(map) and 0 <= nx < len(map[0]) and map[ny][nx] == type:
                        border -= 1
                        if not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((ny, nx))
                perimeter += border
                area += 1
            print(type, area, perimeter)
            answer += area * perimeter

    assert answer != 1368676
    return answer


part2_test_input = part1_test_input

part2_test_output = 1206


def part2(inp: TextIOBase):
    answer = 0

    map = [list(x.strip()) for x in inp.read().strip().splitlines()]
    visited = [[False for _ in range(len(map[0]))] for _ in range(len(map))]

    for y in range(len(map)):
        for x in range(len(map[0])):
            if visited[y][x]:
                continue

            type = map[y][x]
            queue = [(y, x)]
            visited[y][x] = True
            fences_x: dict[float, list[int]] = defaultdict(list)
            fences_y: dict[float, list[int]] = defaultdict(list)
            area = 0
            while queue:
                y2, x2 = queue.pop(0)
                border = 4
                for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    ny, nx = y2 + dy, x2 + dx
                    if 0 <= ny < len(map) and 0 <= nx < len(map[0]) and map[ny][nx] == type:
                        border -= 1
                        if not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((ny, nx))
                    elif dx == 0:
                        fences_y[y2 + ny / 2.0].append(x2)
                    else:
                        fences_x[x2 + nx / 2.0].append(y2)
                area += 1
            print(type, area)
            pprint(fences_x)
            pprint(fences_y)

            sides = 0
            for ys in fences_x.values():
                ys.sort()
                sides += 1
                for i in range(1, len(ys)):
                    if ys[i] - ys[i - 1] > 1:
                        sides += 1
            for xs in fences_y.values():
                xs.sort()
                sides += 1
                for i in range(1, len(xs)):
                    if xs[i] - xs[i - 1] > 1:
                        sides += 1
            print(sides)
            answer += area * sides
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
