from io import StringIO, TextIOWrapper
import sys

part1_test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

part1_test_output = None


def derive(seq: list[int]):
    if all([n == 0 for n in seq]):
        return 0
    else:
        diff = derive([b - a for a, b in zip(seq, seq[1:])])
        return seq[-1] + diff


def part1(inp: TextIOWrapper):
    answer = 0

    seqs = [[int(c) for c in l.strip().split()] for l in inp.readlines()]
    for seq in seqs:
        answer += derive(seq)

    return answer


def derive2(seq: list[int]):
    if all([n == 0 for n in seq]):
        return 0
    else:
        diff = derive2([b - a for a, b in zip(seq, seq[1:])])
        return seq[0] - diff


part2_test_input = part1_test_input

part2_test_output = 2


def part2(inp: TextIOWrapper):
    answer = 0

    seqs = [[int(c) for c in l.strip().split()] for l in inp.readlines()]
    for seq in seqs:
        answer += derive2(seq)

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
