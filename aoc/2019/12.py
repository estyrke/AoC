import functools
from io import TextIOWrapper
import math
from typing import List

part1_test_input = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

part1_test_output = 183

import re
import itertools


def part1(inp: TextIOWrapper):
    moons = [
        list(map(int, re.match("<x=(.*), y=(.*), z=(.*)>", l).groups()))  # type: ignore
        for l in inp.readlines()
    ]
    velocities = [[0, 0, 0] for _ in moons]

    for t in itertools.islice(itertools.count(), 1000):
        for (m1, v1), (m2, v2) in itertools.combinations(zip(moons, velocities), 2):
            for axis in 0, 1, 2:
                if m1[axis] < m2[axis]:
                    v1[axis] += 1
                    v2[axis] -= 1
                elif m2[axis] < m1[axis]:
                    v2[axis] += 1
                    v1[axis] -= 1

        for (m, v) in zip(moons, velocities):
            for axis in 0, 1, 2:
                m[axis] += v[axis]

    energy = sum(
        [sum(map(abs, m)) * sum(map(abs, v)) for m, v in zip(moons, velocities)]
    )
    return energy


part2_test_input = part1_test_input

part2_test_output = 2772


def part2(inp: TextIOWrapper):
    state = [
        [[int(coord), 0] for coord in re.match("<x=(.*), y=(.*), z=(.*)>", l).groups()]  # type: ignore
        for l in inp.readlines()
    ]

    cycles = []
    coord_states = [[moon[axis] for moon in state] for axis in (0, 1, 2)]
    for state in coord_states:
        initial = [list(x) for x in state]
        for t in itertools.count():
            for s1, s2 in itertools.combinations(state, 2):
                if s1[0] < s2[0]:
                    s1[1] += 1
                    s2[1] -= 1
                elif s2[0] < s1[0]:
                    s2[1] += 1
                    s1[1] -= 1

            for s in state:
                s[0] += s[1]

            if state == initial:
                cycles.append(t + 1)
                break

    return functools.reduce(lambda x, y: x * y // math.gcd(x, y), cycles)
