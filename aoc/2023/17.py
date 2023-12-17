from collections import defaultdict
from io import StringIO, TextIOWrapper
import sys
import heapq

part1_test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

part1_test_output = 102

Pos = tuple[int, int]
State = tuple[Pos, int, Pos]


def neigh(map: list[list[int]], pos: State):
    (x, y), straight, (dx, dy) = pos

    res: list[State] = []
    if straight < 2:
        res.append(((x + dx, y + dy), straight + 1, (dx, dy)))
    res.append(((x + dy, y + dx), 0, (dy, dx)))
    res.append(((x - dy, y - dx), 0, (-dy, -dx)))
    return [n for n in res if 0 <= n[0][0] < len(map[0]) and 0 <= n[0][1] < len(map)]


def neigh2(map: list[list[int]], pos: State):
    (x, y), straight, (dx, dy) = pos

    res: list[State] = []
    if straight < 9:
        res.append(((x + dx, y + dy), straight + 1, (dx, dy)))

    if 3 <= straight:
        res.append(((x + dy, y + dx), 0, (dy, dx)))
        res.append(((x - dy, y - dx), 0, (-dy, -dx)))
    return [n for n in res if 0 <= n[0][0] < len(map[0]) and 0 <= n[0][1] < len(map)]


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    lines = [[int(c) for c in l.strip()] for l in inp.readlines()]

    finished = set()
    queue: list[tuple[int, State]] = [
        (0, ((0, 0), 0, (0, 1))),
        (0, ((0, 0), 0, (1, 0))),
    ]

    dist = defaultdict(lambda: 1000000)
    parents: dict[State, State | None] = defaultdict(lambda: None)
    heapq.heapify(queue)
    while queue:
        d, pos = heapq.heappop(queue)
        if pos in finished:
            continue
        finished.add(pos)
        x, y = pos[0]
        if x == len(lines[0]) - 1 and y == len(lines) - 1:
            # Reached end
            p = pos
            while p:
                print(p, lines[p[0][0]][p[0][1]])
                p = parents[p]

            print([d for p, d in dist.items() if p[0] == (0, 2)])
            return d  # + lines[y][x]

        for n in neigh(lines, pos):
            x, y = n[0]
            new_d = d + lines[y][x]
            if new_d < dist[n]:
                dist[n] = new_d
                parents[n] = pos
                heapq.heappush(queue, (new_d, n))

    return answer


part2_test_input = part1_test_input

part2_test_output = 94


def part2(inp: TextIOWrapper):
    lines = [[int(c) for c in l.strip()] for l in inp.readlines()]

    finished = set()
    queue: list[tuple[int, State]] = [
        (0, ((0, 0), 0, (0, 1))),
        (0, ((0, 0), 0, (1, 0))),
    ]

    dist = defaultdict(lambda: 1000000)
    parents: dict[State, State | None] = defaultdict(lambda: None)
    heapq.heapify(queue)
    while queue:
        d, pos = heapq.heappop(queue)
        if pos in finished:
            continue
        finished.add(pos)
        x, y = pos[0]
        if x == len(lines[0]) - 1 and y == len(lines) - 1:
            # Reached end
            p = pos
            while p:
                print(p, lines[p[0][0]][p[0][1]])
                p = parents[p]

            # print([d for p, d in dist.items() if p[0] == (0, 2)])
            return d  # + lines[y][x]

        for n in neigh2(lines, pos):
            x, y = n[0]
            new_d = d + lines[y][x]
            if new_d < dist[n]:
                dist[n] = new_d
                parents[n] = pos
                heapq.heappush(queue, (new_d, n))


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
