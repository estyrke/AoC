from collections import defaultdict
from io import StringIO, TextIOBase
import sys

part1_test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

part1_test_output = 13


def part1(inp: TextIOBase):
    answer = 0

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]
    neigh = defaultdict(int)
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "@":
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == dy == 0:
                            continue
                        neigh[(x + dx, y + dy)] += 1

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "@" and neigh[(x, y)] < 4:
                answer += 1
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = 43


def part2(inp: TextIOBase):
    lines = [list(l.strip()) for l in inp.readlines()]

    answer = 0
    while True:
        neigh = defaultdict(int)
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == "@":
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == dy == 0:
                                continue
                            neigh[(x + dx, y + dy)] += 1
        removed = set()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == "@" and neigh[(x, y)] < 4:
                    removed.add((x, y))

        if len(removed) == 0:
            break

        answer += len(removed)

        for x, y in removed:
            lines[y][x] = "."

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
