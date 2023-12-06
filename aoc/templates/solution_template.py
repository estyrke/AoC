from io import StringIO, TextIOWrapper
import sys

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = None

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
