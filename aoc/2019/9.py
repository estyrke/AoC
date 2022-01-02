from io import TextIOWrapper
import math
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = Machine.from_str(inp.read()).run([1])
    assert len(answer) == 1
    return answer[0]


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = Machine.from_str(inp.read()).run([2])
    assert len(answer) == 1
    return answer[0]
