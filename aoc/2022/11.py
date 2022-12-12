from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input
from parse import compile

part1_test_input = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

part1_test_output = 10605


START = compile("Starting items: {}")
OP = compile("Operation: new = {}")
TEST = compile("Test: divisible by {:d}")
TRUE = compile("If true: throw to monkey {:d}")
FALSE = compile("If false: throw to monkey {:d}")
MUL = compile("old * {:d}")
ADD = compile("old + {:d}")


class Monkey:
    def __init__(self, num, lines) -> None:
        self.num = num
        i = 0
        assert lines[i].startswith("Monkey ")
        self.items = [int(x) for x in START.parse(lines[i + 1]).fixed[0].split(", ")]  # type: ignore
        op = OP.parse(lines[i + 2]).fixed[0]  # type: ignore
        if op == "old * old":
            self.op = lambda x: x * x
        elif (mul := MUL.parse(op)) is not None:
            self.op = lambda x: x * mul.fixed[0]  # type: ignore
        elif (add := ADD.parse(op)) is not None:
            self.op = lambda x: x + add.fixed[0]  # type: ignore
        else:
            raise RuntimeError("Unknown op " + op)
        self.test = TEST.parse(lines[i + 3]).fixed[0]  # type: ignore
        self.t = TRUE.parse(lines[i + 4]).fixed[0]  # type: ignore
        self.f = FALSE.parse(lines[i + 5]).fixed[0]  # type: ignore
        self.t_test = lambda x: x % self.test == 0
        self.f_test = lambda x: x % self.test != 0
        self.inspected = 0

    def turn(self, monkeys):
        # print(f"Monkey {self.num} {self.items}")
        for worry in self.items:
            self.inspected += 1
            worry = self.op(worry)
            worry //= 3
            if worry % self.test == 0:
                monkeys[self.t].items.append(worry)
            else:
                monkeys[self.f].items.append(worry)
        self.items = []

    def turn2(self, monkeys, modulus: int):
        # print(f"Monkey {self.num} {self.items}")
        self.inspected += len(self.items)
        items = map(self.op, self.items)
        # print("i", list(items))
        t_list = []
        f_list = []
        for x in [self.op(x) % modulus for x in self.items]:
            t_list.append(x) if x % self.test == 0 else f_list.append(x)
        # print(t_list)
        # print(f_list)

        monkeys[self.t].items.extend(t_list)
        monkeys[self.f].items.extend(f_list)
        self.items = []


def part1(inp: TextIOWrapper):
    answer = None

    monkeys = []

    lines = [l.strip() for l in inp.readlines()]

    for i in range(0, len(lines), 7):
        monkeys.append(Monkey(i // 7, lines[i : i + 6]))

    for i in range(20):
        for m in monkeys:
            m.turn(monkeys)

    rank = sorted(monkeys, key=lambda x: x.inspected, reverse=True)
    for m in rank:
        print(m.num, m.inspected)

    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return rank[0].inspected * rank[1].inspected


part2_test_input = part1_test_input

part2_test_output = 2713310158


def part2(inp: TextIOWrapper):
    answer = None

    monkeys = []

    lines = [l.strip() for l in inp.readlines()]

    for i in range(0, len(lines), 7):
        monkeys.append(Monkey(i // 7, lines[i : i + 6]))

    modulus = math.prod([m.test for m in monkeys])

    for i in range(10000):
        if i % 1000 == 0:
            print(i)
        for m in monkeys:
            m.turn2(monkeys, modulus)

    rank = sorted(monkeys, key=lambda x: x.inspected, reverse=True)
    for m in rank:
        print(m.num, m.items, m.inspected)

    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return rank[0].inspected * rank[1].inspected
