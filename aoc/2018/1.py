from io import StringIO, TextIOBase
from itertools import cycle
import sys

part1_test_input = """+1
-2
+3
+1"""

part1_test_output = 3


def part1(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        answer += int(line)
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = 0
    changes = [int(l) for l in inp.readlines()]

    seen = set()
    for change in cycle(changes):
        answer += change
        if answer in seen:
            break
        seen.add(answer)
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
