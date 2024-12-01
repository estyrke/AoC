from io import StringIO, TextIOWrapper
import sys

part1_test_input = """3   4
4   3
2   5
1   3
3   9
3   3"""

part1_test_output = 11


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    lines = [l for l in inp.readlines()]

    left = [line.split()[0] for line in lines]
    right = [line.split()[1] for line in lines]

    answer = sum([abs(int(l) - int(r)) for l, r in zip(sorted(left), sorted(right))])

    return answer


part2_test_input = part1_test_input

part2_test_output = 31


def part2(inp: TextIOWrapper):
    answer = None
    lines = [l for l in inp.readlines()]

    left = [line.split()[0] for line in lines]
    right = [line.split()[1] for line in lines]

    def count(l, right):
        return sum([1 for r in right if r == l])

    answer = sum([int(l) * count(l, right) for l in left])

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
