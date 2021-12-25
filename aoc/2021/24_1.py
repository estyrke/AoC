from io import TextIOWrapper
import math
from typing import Optional

###
# # ## --- Day 24: Arithmetic Logic Unit ---
#
# [Magic smoke](https://en.wikipedia.org/wiki/Magic_smoke) starts
# leaking from the submarine's [arithmetic logic
# unit](https://en.wikipedia.org/wiki/Arithmetic_logic_unit) (ALU).
# Without the ability to perform basic arithmetic and logic functions,
# the submarine can't produce cool patterns with its Christmas lights!
#
# It also can't navigate. Or run the oxygen system.
#
# Don't worry, though - you *probably* have enough oxygen left to give
# you enough time to build a new ALU.
#
# The ALU is a four-dimensional processing unit: it has integer
# variables `w`, `x`, `y`, and `z`. These variables all start with the
# value `0`. The ALU also supports *six instructions*:
#
# * `inp a` - Read an input value and write it to variable `a`.
# * `add a b` - Add the value of `a` to the value of `b`, then store the
# result in variable `a`.
# * `mul a b` - Multiply the value of `a` by the value of `b`, then
# store the result in variable `a`.
# * `div a b` - Divide the value of `a` by the value of `b`, truncate
# the result to an integer, then store the result in variable `a`.
# (Here, "truncate" means to round the value toward zero.)
# * `mod a b` - Divide the value of `a` by the value of `b`, then store
# the *remainder* in variable `a`. (This is also called the
# [modulo](https://en.wikipedia.org/wiki/Modulo_operation) operation.)
# * `eql a b` - If the value of `a` and `b` are equal, then store the
# value `1` in variable `a`. Otherwise, store the value `0` in variable
# `a`.
#
#
# In all of these instructions, `a` and `b` are placeholders; `a` will
# always be the variable where the result of the operation is stored
# (one of `w`, `x`, `y`, or `z`), while `b` can be either a variable or
# a number. Numbers can be positive or negative, but will always be
# integers.
#
# The ALU has no *jump* instructions; in an ALU program, every
# instruction is run exactly once in order from top to bottom. The
# program halts after the last instruction has finished executing.
#
# (Program authors should be especially cautious; attempting to execute
# `div` with `b=0` or attempting to execute `mod` with `a<0` or `b<=0`
# will cause the program to crash and might even damage the ALU. These
# operations are never intended in any serious ALU program.)
#
# For example, here is an ALU program which takes an input number,
# negates it, and stores it in `x`:
#
#
# ```
# inp x
# mul x -1
#
# ```
#
# Here is an ALU program which takes two input numbers, then sets `z` to
# `1` if the second input number is three times larger than the first
# input number, or sets `z` to `0` otherwise:
#
#
# ```
# inp z
# inp x
# mul z 3
# eql z x
#
# ```
#
# Here is an ALU program which takes a non-negative integer as input,
# converts it into binary, and stores the lowest (1's) bit in `z`, the
# second-lowest (2's) bit in `y`, the third-lowest (4's) bit in `x`, and
# the fourth-lowest (8's) bit in `w`:
#
#
# ```
# inp w
# add z w
# mod z 2
# div w 2
# add y w
# mod y 2
# div w 2
# add x w
# mod x 2
# div w 2
# mod w 2
#
# ```
#
# Once you have built a replacement ALU, you can install it in the
# submarine, which will immediately resume what it was doing when the
# ALU failed: validating the submarine's *model number*. To do this, the
# ALU will run the MOdel Number Automatic Detector program (MONAD, your
# puzzle input).
#
# Submarine model numbers are always *fourteen-digit numbers* consisting
# only of digits `1` through `9`. The digit `0` *cannot* appear in a
# model number.
#
# When MONAD checks a hypothetical fourteen-digit model number, it uses
# fourteen separate `inp` instructions, each expecting a *single digit*
# of the model number in order of most to least significant. (So, to
# check the model number `13579246899999`, you would give `1` to the
# first `inp` instruction, `3` to the second `inp` instruction, `5` to
# the third `inp` instruction, and so on.) This means that when
# operating MONAD, each input instruction should only ever be given an
# integer value of at least `1` and at most `9`.
#
# Then, after MONAD has finished running all of its instructions, it
# will indicate that the model number was *valid* by leaving a `0` in
# variable `z`. However, if the model number was *invalid*, it will
# leave some other non-zero value in `z`.
#
# MONAD imposes additional, mysterious restrictions on model numbers,
# and legend says the last copy of the MONAD documentation was eaten by
# a [tanuki](https://en.wikipedia.org/wiki/Japanese_raccoon_dog). You'll
# need to *figure out what MONAD does* some other way.
#
# To enable as many submarine features as possible, find the largest
# valid fourteen-digit model number that contains no `0` digits. *What
# is the largest model number accepted by MONAD?*
###

test_input = """"""

test_output = None


code = """
stack = [0]

w = serial[0]
x = int((z % 26) + 12 != w)
z = z * (25 * x + 1) + (w + 7) * x

w = serial[1]
x = int((z % 26) + 13 != w)
z = z * (25 * x + 1) + (w + 8) * x

w = serial[2]
x = int((z % 26) + 13 != w)
z = z * (25 * x + 1) + (w + 10) * x

w = serial[3]
x = int((z % 26) + -2 != w)
z //= 26
z = z * (25 * x + 1) + (w + 4) * x

w = serial[4]
x = int((z % 26) + -10 != w)
z //= 26
z = z * (25 * x + 1) + (w + 4) * x

w = serial[5]
x = int((z % 26) + 13 != w)
z = z * (25 * x + 1) + (w + 6) * x

w = serial[6]
x = int((z % 26) + -14 != w)
z //= 26
z = z * (25 * x + 1) + (w + 11) * x

w = serial[7]
x = int((z % 26) + -5 != w)
z //= 26
z = z * (25 * x + 1) + (w + 13) * x

w = serial[8]
x = int((z % 26) + 15 != w)
z = z * (25 * x + 1) + (w + 0) * x

w = serial[9]
x = int((z % 26) + 15 != w)
z = z * (25 * x + 1) + (w + 8) * x

w = serial[10]
x = int((z % 26) + -14 != w)
z //= 26
z = z * (25 * x + 1) + (w + 4) * x

w = serial[11]
x = int((z % 26) + 10 != w)
z = z * (25 * x + 1) + (w + 13) * x

w = serial[12]
x = int((z % 26) + -14 != w)
z //= 26
z = z * (25 * x + 1) + (w + 4) * x

w = serial[13]
x = int((z % 26) + -5 != w)
z //= 26
z = z * (25 * x + 1) + (w + 14) * x
"""

code2 = """
w = serial[0]
stack.append(w + 7)

w = serial[1]
stack.append(w + 8)

w = serial[2]
stack.append(w + 10)

w = serial[3]
if stack.pop() + -2 != w:  #serial[2] + 8 = serial[3]
    stack.append(w + 4)

w = serial[4]
if stack.pop() + -10 != w:
    stack.append(w + 4)

w = serial[5]
stack.append(w + 6)

w = serial[6]
if stack.pop() + -14 != w:
    stack.append(w + 11)

w = serial[7]
if stack.pop() + -5 != w:
    stack.append(w + 13)

w = serial[8]
stack.append(w + None)

w = serial[9]
stack.append(w + 8)

w = serial[10]
if stack.pop() + -14 != w:
    stack.append(w + 4)

w = serial[11]
stack.append(w + 13)

w = serial[12]
if stack.pop() + -14 != w:
    stack.append(w + 4)

w = serial[13]
if stack.pop() + -5 != w:
    stack.append(w + 14)
"""


def tryeval(x: str):
    try:
        return str(eval(x))
    except NameError:
        return x


def tryint(x: str) -> Optional[int]:
    try:
        return int(x)
    except ValueError:
        return None


def solve(inp: TextIOWrapper):
    print_constraints(inp)

    serial = [9] * 14

    # serial[2] + 8 == serial[3]
    serial[2] = 1
    serial[3] = 9
    # serial[1] - 2 == serial[4]
    serial[1] = 9
    serial[4] = 7
    # serial[5] - 8 == serial[6]
    serial[5] = 9
    serial[6] = 1
    # serial[0] + 2 == serial[7]
    serial[0] = 7
    serial[7] = 9
    # serial[9] - 6 == serial[10]
    serial[9] = 9
    serial[10] = 3
    # serial[11] - 1 == serial[12]
    serial[11] = 9
    serial[12] = 8
    # serial[8] - 4 == serial[13]
    serial[8] = 9
    serial[13] = 5

    return "".join(map(str, serial))


def print_constraints(inp):
    instrs = []
    i = 0
    a = None
    b = None
    denom = None
    stack = [(None, 0)]
    for j, line in enumerate(inp.readlines()):
        instr, args = line.strip().split(maxsplit=1)
        args = args.split()

        if instr == "inp":
            # instrs.append(f"{args[0]} = serial[{i}]")
            denom = None
            a = None
            b = None
            # values[args[0]] = f"inp[{i}]"
            i += 1
        elif instr == "add":
            if args[0] == "x" and tryint(args[1]) is not None:
                # instrs.append(f"a = {args[1]}")
                a = int(args[1])
            if args[0] == "y":
                arg2 = tryint(args[1])
                if arg2 is not None:
                    # Happens multiple times, but we always want the last time
                    # instrs.append(f"b = {args[1]}")
                    b = int(args[1])
            if args[0] == "z" and args[1] == "y":
                if denom != 1:
                    assert a <= 9
                    prev_i, val = stack.pop()
                    instrs.append(f"serial[{prev_i}] + {val + a} == serial[{i-1}]")
                    indent = "    "
                else:
                    assert a > 9
                    indent = ""
                    stack.append((i - 1, b))

                # instrs.append(f"x = int((z % 26) + {a} != w)")

                # instrs.append(f"{indent}stack.append(({i}, {b}))")
                # instrs.append("")
            # instrs.append(f"{args[0]} += {args[1]}")
            # if args[1].isdigit() or args[1][0] == "-":
            #    values[args[0]] = tryeval(f"({values[args[0]]}) + {args[1]}")
            # else:
            #    values[args[0]] = tryeval(f"({values[args[0]]}) + ({values[args[1]]})")
        elif instr == "mul":
            pass  # instrs.append(f"{args[0]} *= {args[1]}")
            # if args[1] == "0":
            #    values[args[0]] = "0"
            # elif args[1] == "1":
            #    pass
            # elif tryeval(values[args[0]]) == "0":
            #    values[args[0]] = "0"
            # elif tryeval(values[args[0]]) == "1":
            #    values[args[0]] = tryeval(args[1])
            # elif args[1].isdigit() or args[1][0] == "-":
            #    values[args[0]] = tryeval(f"({values[args[0]]}) * {args[1]}")
            # else:
            #    values[args[0]] = tryeval(f"({values[args[0]]}) * ({values[args[1]]})")
        elif instr == "div":
            if args[0] == "z":
                # instrs.append(f"denom = {int(args[1])}")
                denom = int(args[1])
            # instrs.append(f"{args[0]} //= {args[1]}")
            # if tryeval(args[1]) == 1:
            #    pass
            # elif args[1].isdigit() or args[1][0] == "-":
            #    values[args[0]] = tryeval(f"({values[args[0]]}) // {args[1]}")
            # else:
            #    values[args[0]] = tryeval(f"({values[args[0]]}) // ({values[args[1]]})")
        elif instr == "mod":
            pass  # instrs.append(f"{args[0]} %= {args[1]}")
            # if args[1].isdigit() or args[1][0] == "-":
            #    values[args[0]] = tryeval(f"({values[args[0]]}) % {args[1]}")
            # else:
            #    values[args[0]] = tryeval(f"({values[args[0]]}) % ({values[args[1]]})")
        else:
            assert instr == "eql"
            # instrs.append(f"{args[0]} = int({args[0]} == {args[1]})")
            # arg1 = tryeval(values[args[0]])
            #
            # if args[1].isdigit() or args[1][0] == "-":
            #    values[args[0]] = tryeval(f"int(({values[args[0]]}) == {args[1]})")
            # else:
            #    values[args[0]] = tryeval(
            #        f"int(({values[args[0]]}) == ({values[args[1]]}))"
            #    )
        # print(len(values["z"]))
        # if len(values["z"]) > 300:
        #    print(i, values["z"])
        #    break

    print("\n".join(instrs))
    # lines = [l for l in inp.readlines()]

    valid = {"x": None, "y": None, "z": 0, "w": None}


def old(instrs):
    prog = "\n".join(instrs)

    code = compile(prog, "hej", "exec")
    print(prog)
    serial = [9] * 14
    while True:
        loc = {"serial": list(serial), "x": 0, "y": 0, "z": 0, "w": 0}
        exec(code, loc)
        print(loc["w"], loc["x"], loc["y"], loc["z"], serial)
        if loc["z"] == 0:
            return int("".join(map(str, serial)))
        for pos in range(len(serial) - 1, -1, -1):
            serial[pos] -= 1
            if serial[pos] > 0:
                break
            else:
                serial[pos] = 9

    return None
