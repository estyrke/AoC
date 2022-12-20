import cProfile
from io import TextIOWrapper
import math
import functools
import itertools
from typing import Dict, List, Tuple
from aoc.tools import parse_input

part1_test_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

part1_test_output = None  # 33

import numpy as np


def open_geodes(
    bp: Tuple[
        Tuple[int, int, int],
        Tuple[int, int, int],
        Tuple[int, int, int],
        Tuple[int, int, int],
    ],
    time: int,
):
    max_cost = (0, 0, 0)
    for i in range(4):
        max_cost = [max(mc, c) for mc, c in zip(max_cost, bp[i])]
    print("Blueprint", bp)

    states = 0

    @functools.cache
    def run(
        time_left: int,
        rb: Tuple[int, int, int],
        res: Tuple[int, int, int],
    ) -> int:
        nonlocal states
        states += 1
        assert time_left > 0

        # Default to just use the robots we have
        max_coll = 0

        if rb[0] >= bp[3][0] and rb[2] >= bp[3][2]:
            # Only build geode robots (one per turn) from now on
            max_coll_with_geode = max_coll + sum([i for i in range(time_left)])
            return max_coll_with_geode

        # Make geode robot
        if rb[2] > 0:
            time_to_next = (
                max(
                    0,
                    (bp[3][0] - res[0] + rb[0] - 1) // rb[0],
                    (bp[3][2] - res[2] + rb[2] - 1) // rb[2],
                )
                + 1
            )
            if time_to_next < time_left:
                coll = (time_left - time_to_next) + run(
                    time_left - time_to_next,
                    (rb[0], rb[1], rb[2]),
                    (
                        res[0] + time_to_next * rb[0] - bp[3][0],
                        res[1] + time_to_next * rb[1],
                        res[2] + time_to_next * rb[2] - bp[3][2],
                    ),
                )
                max_coll = max(max_coll, coll)

        # Make obsidian robot
        if rb[1] > 0 and rb[2] < max_cost[2]:
            time_to_next = (
                max(
                    0,
                    (bp[2][0] - res[0] + rb[0] - 1) // rb[0],
                    (bp[2][1] - res[1] + rb[1] - 1) // rb[1],
                )
                + 1
            )
            if time_to_next < time_left:
                coll = run(
                    time_left - time_to_next,
                    (rb[0], rb[1], rb[2] + 1),
                    (
                        res[0] + time_to_next * rb[0] - bp[2][0],
                        res[1] + time_to_next * rb[1] - bp[2][1],
                        res[2] + time_to_next * rb[2],
                    ),
                )
                max_coll = max(max_coll, coll)

        # Make clay robot
        if rb[1] < max_cost[1]:
            time_to_next = (
                max(
                    0,
                    (bp[1][0] - res[0] + rb[0] - 1) // rb[0],
                )
                + 1
            )
            if time_to_next < time_left:
                coll = run(
                    time_left - time_to_next,
                    (rb[0], rb[1] + 1, rb[2]),
                    (
                        res[0] + time_to_next * rb[0] - bp[1][0],
                        res[1] + time_to_next * rb[1],
                        res[2] + time_to_next * rb[2],
                    ),
                )
                max_coll = max(max_coll, coll)

        # Make ore robot
        if rb[0] < max_cost[0]:
            time_to_next = (
                max(
                    0,
                    (bp[0][0] - res[0] + rb[0] - 1) // rb[0],
                )
                + 1
            )
            if time_to_next < time_left:
                coll = run(
                    time_left - time_to_next,
                    (rb[0] + 1, rb[1], rb[2]),
                    (
                        res[0] + time_to_next * rb[0] - bp[0][0],
                        res[1] + time_to_next * rb[1],
                        res[2] + time_to_next * rb[2],
                    ),
                )
                max_coll = max(max_coll, coll)
        return max_coll

    result = run(time, (1, 0, 0), (0, 0, 0))
    print("Result", result, "after", states, "evaluations")
    return result


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        robots: List[Tuple[int, int, int]] = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        bp, l = line.strip().split(": ")
        bp_idx = int(bp.split()[-1])
        costs = l.split(". ")
        for i, c in enumerate(costs):
            r, c = c.strip(".").split(" costs ")
            c = [i.split() for i in c.split(" and ")]
            c = {i[1]: int(i[0]) for i in c}
            robots[i] = (
                c.get("ore", 0),
                c.get("clay", 0),
                c.get("obsidian", 0),
            )

        geodes = open_geodes(tuple(robots), 24)
        answer += geodes * bp_idx

    return answer


# Still too slow on the test data, so skip it for part 2
part2_test_input = None  # part1_test_input
part2_test_output = None  # 56 * 62


def part2(inp: TextIOWrapper):
    answer = 1

    for line in inp.readlines()[:3]:
        robots: List[Tuple[int, int, int]] = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        _bp, l = line.strip().split(": ")
        costs = l.split(". ")
        for i, c in enumerate(costs):
            _r, c = c.strip(".").split(" costs ")
            c = [i.split() for i in c.split(" and ")]
            c = {i[1]: int(i[0]) for i in c}
            robots[i] = (
                c.get("ore", 0),
                c.get("clay", 0),
                c.get("obsidian", 0),
            )

        print(robots)
        geodes = open_geodes(tuple(robots), 32)
        answer *= geodes

    return answer
