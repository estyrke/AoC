from io import TextIOWrapper
from itertools import permutations
import math
from .intcode import Machine

part1_test_input = """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"""

part1_test_output = 43210


def part1(inp: TextIOWrapper):
    answer = None

    m = Machine.from_str(inp.read())

    max_signal = 0
    for phases in permutations([0, 1, 2, 3, 4]):
        signal = 0
        for i in range(5):
            m.reset()
            signal = m.run([phases[i], signal])[0]

        if signal > max_signal:
            max_signal = signal
    return max_signal


part2_test_input = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"""

part2_test_output = 139629729


def part2(inp: TextIOWrapper):
    code = inp.read()

    max_signal = 0
    for phases in permutations([5, 6, 7, 8, 9]):
        ms = [Machine.from_str(code) for _ in range(5)]

        for i in range(5):
            ms[i].run([phases[i]])

        signal = 0
        while not ms[0].halted:
            for i in range(5):
                signal = ms[i].run([signal])[0]

        if signal > max_signal:
            max_signal = signal
    return max_signal
