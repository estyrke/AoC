from functools import cache
from io import StringIO, TextIOBase
import sys
from typing import Callable

part1_test_input = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

part1_test_output = None


def part1(inp: TextIOBase):
    new_poses = [0] * 10
    test_moves = part1_test_input.splitlines()
    for pos in range(10):
        new_poses[deal(10, pos, test_moves)] = pos
    assert new_poses == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

    # return deal(10_007, 2019, inp.readlines())
    a, b = compose(10_007, inp.readlines())
    return (a * 2019 + b) % 10_007


def deal(size, pos, moves):
    for line in moves:
        if line.startswith("deal into"):
            pos = size - pos - 1
        elif line.startswith("cut "):
            pos -= int(line.split()[1])
            pos %= size
        elif line.startswith("deal with increment "):
            inc = int(line.split()[3])
            pos *= inc
            pos %= size
    return pos


def compose(size, moves):
    a, b = 1, 0
    for line in moves:
        if line.startswith("deal into"):
            # f(x) = -1 * x - 1 (mod size)
            a *= -1
            a %= size
            b = (b * -1 - 1) % size
        elif line.startswith("cut "):
            cut = int(line.split()[1])
            # f(x) = x - cut (mod size)
            b = (b - cut) % size
        elif line.startswith("deal with increment "):
            inc = int(line.split()[3])
            # f(x) = x * inc (mod size)
            a = (a * inc) % size
            b = (b * inc) % size
    return a, b


@cache
def deal_reverse(size: int, pos: int) -> int:
    first_pos = pos
    for line in reversed(moves):
        old_pos = pos
        if line.startswith("deal into"):
            pos = size - pos - 1
            # print(f"{old_pos=} <- {size=} - {old_pos=} - 1 = {pos}")
        elif line.startswith("cut "):
            pos += int(line.split()[1])
            pos %= size
            # print(f"{old_pos=} <- {old_pos=} + {int(line.split()[1])} = {pos}")
        elif line.startswith("deal with increment "):
            inc = int(line.split()[3])
            new_pos = pos
            # print(f"{pos=} {inc=} {divmod(pos, inc)=}")
            shift = inc
            while pos % inc != shift % inc:
                new_pos += size
                shift -= size % inc
            # print(f"{pos=} {inc=} {size%inc=} {shift=} {new_pos=} {new_pos//inc=}")
            # assert shift >= 0
            pos = new_pos // inc
            # print(f"{old_pos=} <- {new_pos=} // {inc=} = {pos}")
            # pos %= size

    # print(f"{first_pos=} <- {pos}")
    return pos


def compile_moves(size: int) -> Callable:
    code = ["def compiled_func(pos):"]
    for line in reversed(moves):
        if line.startswith("deal into"):
            code.append(f"    pos = {size} - pos - 1")
        elif line.startswith("cut "):
            code.append(f"    pos += {int(line.split()[1])}")
            code.append(f"    pos %= {size}")
        elif line.startswith("deal with increment "):
            inc = int(line.split()[3])
            code.append("    new_pos = pos")
            code.append(f"    shift = {inc}")
            code.append(f"    while pos % {inc} != shift % {inc}:")
            code.append(f"        new_pos += {size}")
            code.append(f"        shift -= {size % inc}")
            code.append(f"    pos = new_pos // {inc}")

    code.append("    return pos")
    code_str = "\n".join(code)
    exec_globals = {}
    exec_locals = {}
    exec(code_str, exec_globals, exec_locals)
    print(code_str)
    return exec_locals["compiled_func"]


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    if IS_TEST:
        return None
    moves = inp.readlines()
    answer = None

    size = 119_315_717_514_047
    iters = 101_741_582_076_661

    a, b = compose(size, moves)

    a_k = pow(a, iters, size)
    b = b * (1 - a_k) * pow(1 - a, -1, size)
    b %= size
    a = a_k

    print(f"{a=}, {b=}")

    answer = (2020 - b) * pow(a, -1, size) % size

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
