from collections import defaultdict
from io import StringIO, TextIOWrapper
import sys
from matplotlib import pyplot as plt
from scipy import sparse
import numpy as np

part1_test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

part1_test_output = 62
IS_TEST: bool


def part1(inp: TextIOWrapper):
    answer = None

    x = 0
    y = 0
    dug = {}
    for line in inp.readlines():
        dir, n, col = line.strip().split()
        for i in range(int(n)):
            dug[(x, y)] = 1  # col.strip("()")
            if dir == "U":
                y -= 1
            elif dir == "D":
                y += 1
            elif dir == "L":
                x -= 1
            else:
                assert dir == "R"
                x += 1

    min_y = min([y for (x, y), c in dug.items()])
    min_x = min([x for (x, y), c in dug.items()])
    img = sparse.coo_array(
        (
            [c for (x, y), c in dug.items()],
            (
                [y - min_y for (x, y), c in dug.items()],
                [x - min_x for (x, y), c in dug.items()],
            ),
        )
    ).A

    from skimage.morphology import flood_fill

    if IS_TEST:  # noqa: F821
        img = flood_fill(img, (1, 1), 1)
    else:
        img = flood_fill(img, (213, 156), 1)

    # print(dug)

    plt.imshow(img)
    plt.show()
    answer = np.count_nonzero(img)
    assert answer not in [29725]
    return answer


part2_test_input = part1_test_input

part2_test_output = 952408144115


def part2(inp: TextIOWrapper):
    x = 0
    y = 0
    dug = defaultdict(dict)
    instr = [int(line.strip().split()[-1][2:-1], 16) for line in inp.readlines()]
    instr = [({0: "R", 1: "D", 2: "L", 3: "U"}[col % 16], col // 16) for col in instr]

    answer = 0
    for i, (dir, n) in enumerate(instr):
        for j in range(1, int(n)):
            if dir == "U":
                dug[y - j][x] = (1, True)
            elif dir == "D":
                dug[y + j][x] = (1, True)
        if dir == "U":
            y -= n
        elif dir == "D":
            y += n
        elif dir == "L":
            x -= n
            if instr[i - 1][0] == instr[i + 1][0]:
                dug[y][x] = (n + 1, True)
            else:
                dug[y][x] = (n + 1, False)
        elif dir == "R":
            if instr[i - 1][0] == instr[i + 1][0]:
                dug[y][x] = (n + 1, True)
            else:
                dug[y][x] = (n + 1, False)
            x += n
    for y, ts_uns in dug.items():
        ts = sorted(ts_uns.items())
        inside = False
        x = 0
        for x2, (width, flip) in ts:
            answer += width
            if inside:
                answer += x2 - x
            if flip:
                inside = not inside
            x = x2 + width
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
