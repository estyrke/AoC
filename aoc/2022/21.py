from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

part1_test_output = 152


def evaluate(monkeys: dict, root: str):
    if type(monkeys[root]) != int:
        expr, operands = monkeys[root]
        l = {k: evaluate(monkeys, k) for k in operands}
        monkeys[root] = eval(expr, l)

    return monkeys[root]


def part1(inp: TextIOWrapper):
    answer = None
    monkeys = {}
    for line in inp.readlines():
        m, mexpr = line.strip().split(": ")
        es = mexpr.split()
        if len(es) == 1:
            monkeys[m] = int(mexpr)
        else:
            monkeys[m] = mexpr.replace("/", "//"), (es[0], es[2])

    answer = evaluate(monkeys, "root")

    return answer


part2_test_input = part1_test_input

part2_test_output = 301
from z3 import *


def part2(inp: TextIOWrapper):
    answer = None
    monkeys = {}
    for line in inp.readlines():
        m, mexpr = line.strip().split(": ")
        es = mexpr.split()
        if len(es) == 1:
            monkeys[m] = int(mexpr)
        else:
            monkeys[m] = mexpr.replace("/", "//").split()

    monkeys["root"][1] = "="
    s = Solver()

    m_vars = {name: Int(name) for name in monkeys.keys()}
    del monkeys["humn"]

    for name, m in monkeys.items():
        var = m_vars[name]

        if type(m) == int:
            s.add(var == m)
        else:
            v1, op, v2 = m
            v1 = m_vars[v1]
            v2 = m_vars[v2]
            if op == "=":
                s.add(v1 == v2)
            elif op == "+":
                s.add(var == v1 + v2)
            elif op == "-":
                s.add(var == v1 - v2)
            elif op == "*":
                s.add(var == v1 * v2)
            elif op == "//":
                s.add(var == v1 / v2)
            else:
                assert False

    print(s.check())
    m = s.model()
    return m[m_vars["humn"]].as_long()  # type: ignore
