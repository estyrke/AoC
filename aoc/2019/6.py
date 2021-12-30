from io import TextIOWrapper
import math

part1_test_input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

part1_test_output = 42

import functools


def part1(inp: TextIOWrapper):
    answer = None

    orbits = {}
    lines = [l.strip().split(")") for l in inp.readlines()]

    lines.sort()
    for inner, outer in lines:
        assert outer not in orbits
        if outer not in orbits:
            orbits[outer] = inner

    @functools.lru_cache(None)
    def orbcount(outer):
        if outer not in orbits:
            return 0
        else:
            return 1 + orbcount(orbits[outer])

    return sum(orbcount(v) for v in orbits.keys())


part2_test_input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

part2_test_output = 4


def part2(inp: TextIOWrapper):
    orbits = {}
    lines = [l.strip().split(")") for l in inp.readlines()]

    lines.sort()
    for inner, outer in lines:
        assert outer not in orbits
        if outer not in orbits:
            orbits[outer] = inner

    def trace(outer):
        if outer not in orbits:
            return []
        else:
            return trace(orbits[outer]) + [outer]

    you = trace("YOU")
    santa = trace("SAN")

    for i, (y, s) in enumerate(zip(you, santa)):
        if y != s:
            return len(you[i + 1 :]) + len(santa[i + 1 :])
