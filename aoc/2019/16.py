from io import TextIOWrapper
import math
import functools
import itertools
import operator

part1_test_input = """80871224585914546619083218645595"""
part1_test_input = """12345678"""
part1_test_output = 24176176


def duplicate(iterable, n):
    for e in itertools.cycle(iterable):
        yield from itertools.repeat(e, n)


def transform(data, pattern, offset=0):
    for i in range(len(data)):
        s = sum(
            map(
                operator.mul,
                data,
                itertools.islice(duplicate(pattern, offset + i + 1), 1, None),
            )
        )
        if s > 0:
            yield s % 10
        else:
            yield (-s) % 10


def part1(inp: TextIOWrapper):
    data = list(map(int, inp.read().strip()))
    pattern = [0, 1, 0, -1]
    for phase in range(100):
        data = list(transform(data, pattern))
        # print(data)
    return int("".join(map(str, itertools.islice(data, 8))))


part2_test_input = """03081770884921959731165446850517"""

part2_test_output = 53553731


def part2(inp: TextIOWrapper):
    data = list(map(int, inp.read().strip())) * 10000
    message_offset = int("".join(list(map(str, data[:7]))))
    data = data[message_offset:]

    for phase in range(100):
        # The trick here is that the offset is larger than 50% of the total message,
        # which means that any output digit n >= offset will always use a pattern of (n-1) zeroes
        # followed by n ones, and no other part of the pattern will be needed.
        # This implies that the value for output digits >= offset is always the sum of the remaining elements
        # This also means we can calculate the sum once for the whole phase and then just subtract the next
        #  element mod 10 for each successive element.
        s = sum(data) % 10
        for i in range(len(data)):
            data[i], s = s, (s - data[i]) % 10
    return int("".join(map(str, itertools.islice(data, 8))))
