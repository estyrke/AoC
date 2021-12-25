from io import TextIOWrapper
import math
from typing import Optional

###
# ## --- Part Two ---
#
# As the submarine starts booting up things like the [Retro
# Encabulator](https://www.youtube.com/watch?v=RXJKdh1KZ0w), you realize
# that maybe you don't need all these submarine features after all.
#
# *What is the smallest model number accepted by MONAD?*
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
    serial[1] = 3
    serial[4] = 1
    # serial[5] - 8 == serial[6]
    serial[5] = 9
    serial[6] = 1
    # serial[0] + 2 == serial[7]
    serial[0] = 1
    serial[7] = 3
    # serial[9] - 6 == serial[10]
    serial[9] = 7
    serial[10] = 1
    # serial[11] - 1 == serial[12]
    serial[11] = 2
    serial[12] = 1
    # serial[8] - 4 == serial[13]
    serial[8] = 5
    serial[13] = 1

    return "".join(map(str, serial))


def print_constraints(inp):
    instrs = []
    i = 0
    values = {"x": "0", "y": "0", "z": "0", "w": "0"}

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
