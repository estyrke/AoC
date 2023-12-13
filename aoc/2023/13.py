from io import StringIO, TextIOWrapper
from itertools import zip_longest
from pprint import pprint
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


def check_lines(lines: list[str] | list[list[str]]) -> int:
    for y in range(len(lines)):
        half = (len(lines) - y) // 2
        if (len(lines) - y) % 2 != 0:
            # print(f"{y} Not even, skipping")
            continue
        # print(f"y: {y}, half: {half}, y+half:{y+half}, -half-1:{-half-1}")
        # print(
        #    list(
        #        # l1 == l2                for l1, l2 in
        #        zip(lines[:half], lines[-y - 1 : -y - half - 1 : -1], strict=True)
        #    )
        # )
        # pairs = list(zip(lines[y : y + half], lines[-1 : -half - 1 : -1], strict=True))
        # print(y, list(pairs))
        # print(list(l1 == l2 for l1, l2 in pairs))
        if all(
            l1 == l2
            for l1, l2 in zip(
                lines[y : y + half], lines[-1 : -half - 1 : -1], strict=True
            )
        ):
            # print(100 * (y + half))
            return y + half
        if all(
            l1 == l2
            for l1, l2 in zip(
                lines[:half], lines[-y - 1 : -y - half - 1 : -1], strict=True
            )
        ):
            # print(100 * (y + half))
            return len(lines) - y - half
    return 0


def check_lines2(
    lines: ndarray, ignore_pos: int | None = None
) -> tuple[int, list[tuple[int, int]]]:
    res = 0
    flip_candidates = []
    for y in range(len(lines)):
        half = (len(lines) - y) // 2
        if (len(lines) - y) % 2 != 0:
            continue

        diff_y1 = np.abs(lines[y : y + half, :] - lines[-1 : -half - 1 : -1, :])

        if np.sum(diff_y1) == 0:
            if ignore_pos != y + half:
                res = y + half
        elif np.sum(diff_y1) == 1:
            pt = tuple(list(np.argwhere(diff_y1)[0]))
            flip_candidates.append((pt[0] + y, pt[1]))
        diff_y2 = np.abs(lines[:half, :] - lines[-y - 1 : -y - half - 1 : -1, :])

        if np.sum(diff_y2) == 0:
            if ignore_pos != len(lines) - y - half:
                res = len(lines) - y - half
        elif np.sum(diff_y2) == 1:
            print(y)
            print(list(np.argwhere(diff_y2)))
            pt = tuple(list(np.argwhere(diff_y2)[0]))
            print(pt)
            flip_candidates.append(pt)

    return res, flip_candidates


def part1(inp: TextIOWrapper):
    answer = 0

    lines = []
    cols = []
    for i, line in enumerate(inp.readlines()):
        if not line.strip():
            cols = ["".join(col) for col in cols]
            line_score = check_lines(lines) * 100
            col_score = check_lines(cols)
            if line_score == 0 and col_score == 0:
                print("Sample", i)
                pprint(cols)
                assert False

            if i == 49:
                print(col_score)
                assert col_score == 1

            answer += line_score
            answer += col_score
            lines = []
            cols = []
        else:
            lines.append(line.strip())
            cols = [
                [*col, c] for col, c in zip_longest(cols, line.strip(), fillvalue=[])
            ]

    answer += check_lines(lines) * 100
    answer += check_lines(cols)
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    assert answer not in [22376, 52479]
    return answer


part2_test_input = part1_test_input

part2_test_output = 400


def calc(lines: ndarray):
    line_score, flip_candidates = check_lines2(lines)
    col_score, cflip_candidates = check_lines2(np.transpose(lines))
    flip_candidates.extend((y, x) for x, y in cflip_candidates)
    if line_score == 0 and col_score == 0:
        pprint(lines)
        assert False

    print(f"before: line_score: {line_score}, col_score: {col_score}")
    print(flip_candidates)
    assert len(flip_candidates) == 1

    lines[flip_candidates[0]] = 1 - lines[flip_candidates[0]]
    line_score, _ = check_lines2(lines, line_score)
    col_score, _ = check_lines2(np.transpose(lines), col_score)
    if line_score == 0 and col_score == 0:
        pprint(lines)
        assert False

    print(f"after: line_score: {line_score}, col_score: {col_score}")

    return line_score * 100 + col_score


def part2(inp: TextIOWrapper):
    answer = 0

    lines: list[list[int]] = []
    for i, line in enumerate(inp.readlines()):
        if not line.strip():
            answer += calc(np.array(lines))
            lines = []
        else:
            lines.append([1 if c == "#" else 0 for c in line.strip()])

    answer += calc(np.array(lines))

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
