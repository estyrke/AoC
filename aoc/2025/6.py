from itertools import zip_longest
from functools import reduce
import operator
from io import StringIO, TextIOBase
import sys

part1_test_input = """123 328  51 64\n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  """

part1_test_output = 4277556


def part1(inp: TextIOBase):
    answer = 0

    # for line in inp.readlines():
    lines = [l.split() for l in inp.readlines()]
    problems = zip(*lines)
    for prob in problems:
        op = prob[-1]
        if op == "*":
            answer += reduce(operator.mul, (int(x) for x in prob[:-1]), 1)
        elif op=="+":
            answer += reduce(operator.add, (int(x) for x in prob[:-1]), 0)
        else:
            raise RuntimeError(op)

    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = 3263827


def part2(inp: TextIOBase):
    answer = 0
    lines = [list(l.removesuffix("\n")) for l in inp.readlines()]
    nums = []
    op = None
    for i, col in enumerate(zip_longest(*lines, fillvalue=" ")):
        if all(c == " " for c in col):
            if op == "*":
                answer += reduce(operator.mul, (int(x) for x in nums), 1)
            elif op=="+":
                answer += reduce(operator.add, (int(x) for x in nums), 0)
            else:
                raise RuntimeError(op)
            nums = []
            op=None
        else:
            nums.append("".join(col[:-1]))
            if col[-1] != " ":
                op = col[-1]

    if op == "*":
        answer += reduce(operator.mul, (int(x) for x in nums), 1)
    elif op=="+":
        answer += reduce(operator.add, (int(x) for x in nums), 0)
    else:
        assert op is None
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
