from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

part1_test_output = 13


def correct(p1, p2):
    if type(p1) == int and type(p2) == int:
        if p1 < p2:
            raise ValueError(True)
        if p1 > p2:
            raise ValueError(False)
        return
    elif type(p1) == list and type(p2) == list:
        for v1, v2 in zip(p1, p2):
            correct(v1, v2)
        if len(p1) < len(p2):
            raise ValueError(True)
        if len(p1) > len(p2):
            raise ValueError(False)
        return
    elif type(p1) == list:
        assert type(p2) == int
        correct(p1, [p2])
        return
    elif type(p2) == list:
        assert type(p1) == int
        correct([p1], p2)
        return
    print(type(p1), type(p2))
    assert False


class Comp:
    def __init__(self, l):
        self.l = l

    def __lt__(self, other):
        if type(self.l) == int and type(other) == int:
            return self.l < other
        elif type(self.l) == list and type(other) == list:
            l1 = [Comp(i) for i in self.l]
            l2 = [Comp(i) for i in other]
            return l1 < l2
        elif type(self.l) == list:
            assert type(other) == int
            correct(self.l, [other])
            return
        elif type(other) == list:
            assert type(self.l) == int
            correct([self.l], other)
            return


def correct2(p1, p2):

    return p1 < p2


def part1(inp: TextIOWrapper):
    answer = 0

    pairs = inp.read().split("\n\n")

    for i, p in enumerate(pairs):
        p1, p2 = p.split("\n", 1)
        p1 = eval(p1)
        p2 = eval(p2)
        # p1 = Comp(p1)
        # p2 = Comp(p2)
        try:
            correct(p1, p2)
            assert False
        except ValueError as e:
            if e.args[0]:
                answer += i + 1
        # if correct(p1, p2):
        #    answer += i + 1
    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    assert answer != 7658
    return answer


part2_test_input = part1_test_input

part2_test_output = 140


def sort_packet(p1, p2):
    try:
        correct(p1, p2)
        return 0
    except ValueError as e:
        if e.args[0]:
            return -1
        else:
            return 1


def part2(inp: TextIOWrapper):
    answer = None

    packets = [eval(line.strip()) for line in inp.readlines() if line.strip() != ""]
    packets.append([[2]])
    packets.append([[6]])

    s = sorted(packets, key=functools.cmp_to_key(sort_packet))

    div1 = s.index([[2]]) + 1
    div2 = s.index([[6]]) + 1

    print(div1, div2)
    return div1 * div2
