from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """1
2
-3
3
-2
0
4
"""

part1_test_output = 3


def part1(inp: TextIOWrapper):
    answer = None

    num_init = [(int(l.strip()), i) for i, l in enumerate(inp.readlines())]
    num = list(num_init)
    assert len(set(num)) == len(num)
    for i, (n, idx) in enumerate(num_init):
        curr_pos = num.index((n, idx))
        new_pos = curr_pos + n

        new_pos = new_pos % (len(num) - 1)

        if new_pos == 0:
            new_pos = len(num)
        if not 0 < new_pos <= len(num):
            print(new_pos)
        num = num[:curr_pos] + num[curr_pos + 1 :]
        num = num[:new_pos] + [(n, idx)] + num[new_pos:]

    zero_elem = next(filter(lambda e: e[0] == 0, num))

    zero_pos = num.index(zero_elem)
    p1 = (zero_pos + 1000) % len(num)
    p2 = (zero_pos + 2000) % len(num)
    p3 = (zero_pos + 3000) % len(num)
    answer = num[p1][0] + num[p2][0] + num[p3][0]

    return answer


part2_test_input = part1_test_input

part2_test_output = 1623178306


def part2(inp: TextIOWrapper):
    key = 811589153
    num_init = [(int(l.strip()) * key, i) for i, l in enumerate(inp.readlines())]
    num = list(num_init)
    assert len(set(num)) == len(num)
    for _iter in range(10):
        for i, (n, idx) in enumerate(num_init):
            curr_pos = num.index((n, idx))
            new_pos = curr_pos + n

            new_pos = new_pos % (len(num) - 1)
            if new_pos == 0:
                new_pos = len(num)
            num = num[:curr_pos] + num[curr_pos + 1 :]
            num = num[:new_pos] + [(n, idx)] + num[new_pos:]

    zero_elem = next(filter(lambda e: e[0] == 0, num))

    zero_pos = num.index(zero_elem)
    p1 = (zero_pos + 1000) % len(num)
    p2 = (zero_pos + 2000) % len(num)
    p3 = (zero_pos + 3000) % len(num)
    answer = num[p1][0] + num[p2][0] + num[p3][0]

    return answer
