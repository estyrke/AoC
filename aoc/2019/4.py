from io import TextIOWrapper
import math
from typing import List, Tuple

part1_test_input = """"""

part1_test_output = None


def valid(n: int) -> bool:
    """
    >>> valid(111111)
    True
    >>> valid(223450)
    False
    >>> valid(123789)
    False
    >>> valid(112233)
    True
    >>> valid(123444)
    True
    >>> valid(111122)
    True
    """
    maxd = "0"
    last = "x"
    doubled = False
    for digit in str(n):
        if digit < maxd:
            return False
        maxd = max(maxd, digit)
        if digit == last:
            doubled = True
        last = digit

    return doubled


def valid2(n: int) -> bool:
    """
    >>> valid(111111)
    False
    >>> valid(223450)
    False
    >>> valid(123789)
    False
    >>> valid(112233)
    True
    >>> valid(123444)
    False
    >>> valid(111122)
    True
    """
    maxd = "0"
    last = "x"
    doubled = False
    run = 1
    for digit in str(n):
        if digit < maxd:
            return False
        maxd = max(maxd, digit)
        if digit == last:
            run += 1
        else:
            if run == 2:
                doubled = True
            run = 1
            last = digit

    return doubled or run == 2


def part1(inp: TextIOWrapper):
    minp, maxp = [int(x) for x in inp.read().strip().split("-")]

    return len([n for n in range(minp, maxp + 1) if valid(n)])


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    minp, maxp = [int(x) for x in inp.read().strip().split("-")]

    return len([n for n in range(minp, maxp + 1) if valid2(n)])
