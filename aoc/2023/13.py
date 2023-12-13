from io import StringIO, TextIOWrapper
import sys
import numpy as np
from numpy import ndarray

part1_test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

part1_test_output = 405


def check_lines(lines: ndarray, target_diff=0) -> int:
    for y in range(len(lines)):
        half = (len(lines) - y) // 2
        if (len(lines) - y) % 2 != 0:
            continue

        diff_y1 = lines[y : y + half, :] != lines[-1 : -half - 1 : -1, :]
        if np.sum(diff_y1) == target_diff:
            return y + half

        diff_y2 = lines[:half, :] != lines[-y - 1 : -y - half - 1 : -1, :]
        if np.sum(diff_y2) == target_diff:
            return len(lines) - y - half

    return 0


def part1(inp: TextIOWrapper):
    answer = 0

    for map in inp.read().split("\n\n"):
        lines = np.array([list(l) for l in map.splitlines()])
        line_score = check_lines(lines) * 100
        col_score = check_lines(lines.T)

        answer += line_score + col_score

    return answer


part2_test_input = part1_test_input

part2_test_output = 400


def part2(inp: TextIOWrapper):
    answer = 0

    for map in inp.read().split("\n\n"):
        lines = np.array([list(l) for l in map.splitlines()])
        line_score = check_lines(lines, 1) * 100
        col_score = check_lines(lines.T, 1)

        answer += line_score + col_score

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
