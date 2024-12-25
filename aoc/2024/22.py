from collections import defaultdict
from io import StringIO, TextIOBase
import sys

part1_test_input = """1
10
100
2024"""

part1_test_output = 37327623


def part1(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        init = int(line)
        for i in range(2000):
            init = ((init << 6) ^ init) & (2**24 - 1)
            init = ((init >> 5) ^ init) & (2**24 - 1)
            init = ((init << 11) ^ init) & (2**24 - 1)
        answer += init

    return answer


part2_test_input = """1
2
3
2024"""

part2_test_output = 23


def part2(inp: TextIOBase):
    diff_lists = []
    sum_seqs = defaultdict(int)
    for line in inp.readlines():
        init = int(line)
        diff_lists.append([(init % 10, None)])
        old_init = init % 10
        diff_list = []
        seqs = {}
        for i in range(2000):
            init = ((init << 6) ^ init) & (2**24 - 1)
            init = ((init >> 5) ^ init) & (2**24 - 1)
            init = ((init << 11) ^ init) & (2**24 - 1)
            diff_list.append(init % 10 - old_init)
            old_init = init % 10
            diff_list = diff_list[-4:]
            if len(diff_list) == 4:
                if tuple(diff_list) not in seqs:
                    seqs[tuple(diff_list)] = init % 10
        for k, v in seqs.items():
            sum_seqs[k] += v

    print(sum_seqs)
    print(diff_lists)
    return max(sum_seqs.values())


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
