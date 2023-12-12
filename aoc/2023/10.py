from io import StringIO, TextIOWrapper
import sys

import numpy as np

part1_test_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

part1_test_output = 8


def neigh(map: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    if map[pos[1]][pos[0]] == "F":
        return [(pos[0] + 1, pos[1] + 0), (pos[0] + 0, pos[1] + 1)]
    if map[pos[1]][pos[0]] == "J":
        return [(pos[0] + -1, pos[1] + 0), (pos[0] + 0, pos[1] + -1)]
    if map[pos[1]][pos[0]] == "7":
        return [(pos[0] + -1, pos[1] + 0), (pos[0] + 0, pos[1] + 1)]
    if map[pos[1]][pos[0]] == "L":
        return [(pos[0] + 1, pos[1] + 0), (pos[0] + 0, pos[1] + -1)]
    if map[pos[1]][pos[0]] == "-":
        return [(pos[0] + -1, pos[1] + 0), (pos[0] + 1, pos[1] + 0)]
    if map[pos[1]][pos[0]] == "|":
        return [(pos[0] + 0, pos[1] + -1), (pos[0] + 0, pos[1] + 1)]
    if map[pos[1]][pos[0]] == "S":
        ret = []
        for n, ok in (
            ((pos[0] + 1, pos[1]), "7-J"),
            ((pos[0] - 1, pos[1]), "L-F"),
            ((pos[0], pos[1] + 1), "|LJ"),
            ((pos[0], pos[1] - 1), "|F7"),
        ):
            if (
                0 <= n[0] < len(map[0])
                and 0 <= n[1] < len(map)
                and map[n[1]][n[0]] in ok
            ):
                ret.append(n)
        return ret
    print(map[pos[1]][pos[0]])
    assert False


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]

    start = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                start = (x, y)
    assert start is not None

    q: list[tuple[int, tuple[int, int]]] = [(0, start)]
    visited: dict[tuple[int, int], int] = dict()
    while len(q):
        dist, pos = q.pop(0)
        visited[pos] = dist
        for n in neigh(lines, pos):
            if n not in visited:
                q.append((dist + 1, n))
        assert len(q) < 1000000

    answer = max(visited.values())
    assert answer not in [6917]
    return answer


part2_test_input = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

part2_test_output = 8


def part2(inp: TextIOWrapper):
    lines = [list(l.strip()) for l in inp.readlines()]

    start = None
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "S":
                start = (x, y)
    assert start is not None

    q: list[tuple[int, tuple[int, int]]] = [(0, start)]
    visited: dict[tuple[int, int], int] = dict()
    while len(q):
        dist, pos = q.pop(0)
        visited[pos] = dist
        for n in neigh(lines, pos):
            if n not in visited:
                q.append((dist + 1, n))
        assert len(q) < 1000000

    map = np.zeros((len(lines) * 3, len(lines[0]) * 3), dtype=np.uint8)
    print(map.shape)
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if (x, y) not in visited:
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ]
            elif c == "L":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 1, 0],
                    [0, 1, 1],
                    [0, 0, 0],
                ]
            elif c == "J":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 1, 0],
                    [1, 1, 0],
                    [0, 0, 0],
                ]
            elif c == "F":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 0, 0],
                    [0, 1, 1],
                    [0, 1, 0],
                ]
            elif c == "7":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0],
                ]
            elif c == "-":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0],
                ]
            elif c == "|":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                ]
            elif c == "S":
                map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3] = [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0],
                ]

    from skimage.morphology import flood_fill

    map = flood_fill(map, (0, 0), 2)

    answer = 0
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if map[y * 3 : y * 3 + 3, x * 3 : x * 3 + 3].sum() == 0:
                answer += 1
    from matplotlib import pyplot as plt

    # print("\n".join(["".join(l) for l in lines]))

    plt.imshow(map)
    plt.show()

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
