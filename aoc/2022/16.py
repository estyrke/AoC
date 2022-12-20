import cProfile
from io import TextIOWrapper
import math
import functools
import itertools
import pprint
import time
from typing import Dict, List, Tuple
from ..tools import parse_input

part1_test_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

part1_test_output = 1651


def floyd_warshall(G):
    numOfVertices = len(G)
    distance = [[x if x == 1 else 1000 for x in row] for row in G]
    for i in range(numOfVertices):
        distance[i][i] = 0
    for k in range(numOfVertices):
        for i in range(numOfVertices):
            for j in range(numOfVertices):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    return distance


def part1(inp: TextIOWrapper):
    answer = None

    lines = [l.strip().split() for l in inp.readlines()]
    parsed = {
        t[1]: (int(t[4][:-1].split("=")[1]), [u.strip(",") for u in t[9:]])
        for t in lines
    }
    int_to_pos = {i: v for i, v in enumerate(parsed.keys())}
    pos_to_int = {v: i for i, v in enumerate(parsed.keys())}
    valves = {
        pos_to_int[k]: (p, [pos_to_int[n] for n in next])
        for k, (p, next) in parsed.items()
    }
    closed = {v for v in valves.keys()}
    flow = [p for (p, _) in valves.values()]
    graph = [[0 for x in valves] for row in valves]
    for k, (_, next) in valves.items():
        for n in next:
            graph[k][n] = 1
    distance = floyd_warshall(graph)

    answer, state = open_valves(
        flow, distance, pos_to_int["AA"], 30, tuple(sorted(tuple(closed))), 1
    )
    print_state(int_to_pos, state)
    return answer


part2_test_input = part1_test_input
part2_test_output = 1707


def open_valves(
    flow: List[int],
    distance: List[List[int]],
    start_pos: int,
    time: int,
    closed: tuple,
    num_players: int,
):
    @functools.cache
    def make_open(closed: tuple, opened: tuple):
        return tuple(sorted(tuple(set(closed) - set(opened))))

    def targets(pos, time_left, closed: tuple):
        return [
            (i, distance[pos][i])
            for i in closed
            if distance[pos][i] < time_left and flow[i] > 0 and pos != i
        ]

    states = 0

    @functools.cache
    def run(pos: int, time_left: int, closed: tuple, players_left: int):
        nonlocal states
        states += 1
        if players_left == 0:
            return 0, []

        if time_left <= 0:
            next_player, state = run(start_pos, time, closed, players_left - 1)
            return next_player, state

        new_closed = make_open(closed, (pos,))
        max_p, max_state = run(start_pos, time, new_closed, players_left - 1)

        current_p = flow[pos]
        max_state = [
            (pos if current_p else None, None, num_players - players_left, time_left)
        ] + max_state

        t = targets(pos, time_left, closed)
        # print("Targets", t)
        for next, dist in t:
            if current_p == 0:
                # Start pos
                assert pos == start_pos
                new_p, state = run(next, time_left - dist, closed, players_left)
                if new_p > max_p:
                    max_p = new_p
                    max_state = [
                        (None, next, num_players - players_left, time_left)
                    ] + state
            else:
                new_p, state = run(next, time_left - dist - 1, new_closed, players_left)
                if new_p > max_p:
                    max_p = new_p
                    max_state = [
                        (pos, next, num_players - players_left, time_left)
                    ] + state
        return max_p + current_p * (time_left - 1), max_state

    result = run(start_pos, time, closed, num_players)
    return result


def print_state(int_to_pos: Dict[int, str], state: List[Tuple[int, int, int, int]]):
    for opened, next, player, time_left in sorted(state, key=lambda s: -s[-1]):
        if opened is None:
            print(
                f"Player {player+1} starts moving to {int_to_pos.get(next,'nothing')} at {time_left}"
            )
        else:
            print(
                f"Player {player+1} opened {int_to_pos[opened]} and starts moving to {int_to_pos.get(next, 'nothing')} at {time_left}"
            )


def part2(inp: TextIOWrapper):
    lines = [l.strip().split() for l in inp.readlines()]
    parsed = {
        t[1]: (int(t[4][:-1].split("=")[1]), [u.strip(",") for u in t[9:]])
        for t in lines
    }
    int_to_pos = {i: v for i, v in enumerate(parsed.keys())}
    pos_to_int = {v: i for i, v in enumerate(parsed.keys())}
    valves = {
        pos_to_int[k]: (p, [pos_to_int[n] for n in next])
        for k, (p, next) in parsed.items()
    }

    closed = tuple(sorted(v for v in valves.keys() if valves[v][0] > 0))
    flow = [p for p, _ in valves.values()]
    graph = [[0 for x in valves] for row in valves]
    for k, (_, next) in valves.items():
        for n in next:
            graph[k][n] = 1
    distance = floyd_warshall(graph)

    players = 2
    answer, state = open_valves(flow, distance, pos_to_int["AA"], 26, closed, players)
    print_state(int_to_pos, state)
    return answer
