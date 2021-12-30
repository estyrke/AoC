from io import TextIOWrapper
import math
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = None

    memory = list(map(int, inp.read().split(",")))

    answer = Machine(memory).run([1])

    assert sum(answer[:-1]) == 0
    return answer[-1]


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):

    memory = list(map(int, inp.read().split(",")))

    answer = Machine(memory).run([5])

    assert len(answer) == 1
    return answer[0]
