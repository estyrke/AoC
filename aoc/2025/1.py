from aoc.tools import parse_input
from io import StringIO, TextIOBase
import sys

part1_test_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

part1_test_output = 3


def part1(inp: TextIOBase):
    answer = 0
    pos = 50

    for direction, distance in parse_input(inp, "{:.1}{:d}"):
        if direction == "L":
            pos -= distance
        else:
            pos += distance
        pos %= 100
        if pos == 0:
            answer += 1
    return answer


part2_test_input = part1_test_input

part2_test_output = 6


def part2(inp: TextIOBase):
    answer = 0
    pos = 50

    for direction, distance in parse_input(inp, "{:.1}{:d}"):
        if direction == "L":
            if pos == 0:
                td = distance
            else:
                td = 100 - pos + distance
            print("L", distance, td)
            answer += td // 100
            pos -= distance
        else:
            td = pos + distance
            print("R", distance, td)
            answer += td // 100
            pos += distance

        pos %= 100
        print("->", pos)

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
