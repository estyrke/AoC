from io import TextIOWrapper
import math
from typing import Dict, List, Optional, Sequence, Set, Tuple, cast

###
# # ## --- Day 23: Amphipod ---
#
# A group of [amphipods](https://en.wikipedia.org/wiki/Amphipoda) notice
# your fancy submarine and flag you down. "With such an impressive
# shell," one amphipod says, "surely you can help us with a question
# that has stumped our best scientists."
#
# They go on to explain that a group of timid, stubborn amphipods live
# in a nearby burrow. Four types of amphipods live there: *Amber* (`A`),
# *Bronze* (`B`), *Copper* (`C`), and *Desert* (`D`). They live in a
# burrow that consists of a *hallway* and four *side rooms*. The side
# rooms are initially full of amphipods, and the hallway is initially
# empty.
#
# They give you a *diagram of the situation* (your puzzle input),
# including locations of each amphipod (`A`, `B`, `C`, or `D`, each of
# which is occupying an otherwise open space), walls (`#`), and open
# space (`.`).
#
# For example:
#
#
# ```
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
#
# ```
#
# The amphipods would like a method to organize every amphipod into side
# rooms so that each side room contains one type of amphipod and the
# types are sorted `A`-`D` going left to right, like this:
#
#
# ```
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #########
#
# ```
#
# Amphipods can move up, down, left, or right so long as they are moving
# into an unoccupied open space. Each type of amphipod requires a
# different amount of *energy* to move one step: Amber amphipods require
# `1` energy per step, Bronze amphipods require `10` energy, Copper
# amphipods require `100`, and Desert ones require `1000`. The amphipods
# would like you to find a way to organize the amphipods that requires
# the *least total energy*.
#
# However, because they are timid and stubborn, the amphipods have some
# extra rules:
#
# * Amphipods will never *stop on the space immediately outside any
# room*. They can move into that space so long as they immediately
# continue moving. (Specifically, this refers to the four open spaces in
# the hallway that are directly above an amphipod starting position.)
# * Amphipods will never *move from the hallway into a room* unless that
# room is their destination room *and* that room contains no amphipods
# which do not also have that room as their own destination. If an
# amphipod's starting room is not its destination room, it can stay in
# that room until it leaves the room. (For example, an Amber amphipod
# will not move from the hallway into the right three rooms, and will
# only move into the leftmost room if that room is empty or if it only
# contains other Amber amphipods.)
# * Once an amphipod stops moving in the hallway, *it will stay in that
# spot until it can move into a room*. (That is, once any amphipod
# starts moving, any other amphipods currently in the hallway are locked
# in place and will not move again until they can move fully into a
# room.)
#
#
# In the above example, the amphipods can be organized using a minimum
# of `*12521*` energy. One way to do this is shown below.
#
# Starting configuration:
#
#
# ```
# #############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########
#
# ```
#
# One Bronze amphipod moves into the hallway, taking 4 steps and using
# `40` energy:
#
#
# ```
# #############
# #...B.......#
# ###B#C#.#D###
#   #A#D#C#A#
#   #########
#
# ```
#
# The only Copper amphipod not in its side room moves there, taking 4
# steps and using `400` energy:
#
#
# ```
# #############
# #...B.......#
# ###B#.#C#D###
#   #A#D#C#A#
#   #########
#
# ```
#
# A Desert amphipod moves out of the way, taking 3 steps and using
# `3000` energy, and then the Bronze amphipod takes its place, taking 3
# steps and using `30` energy:
#
#
# ```
# #############
# #.....D.....#
# ###B#.#C#D###
#   #A#B#C#A#
#   #########
#
# ```
#
# The leftmost Bronze amphipod moves to its room using `40` energy:
#
#
# ```
# #############
# #.....D.....#
# ###.#B#C#D###
#   #A#B#C#A#
#   #########
#
# ```
#
# Both amphipods in the rightmost room move into the hallway, using
# `2003` energy in total:
#
#
# ```
# #############
# #.....D.D.A.#
# ###.#B#C#.###
#   #A#B#C#.#
#   #########
#
# ```
#
# Both Desert amphipods move into the rightmost room using `7000`
# energy:
#
#
# ```
# #############
# #.........A.#
# ###.#B#C#D###
#   #A#B#C#D#
#   #########
#
# ```
#
# Finally, the last Amber amphipod moves into its room, using `8`
# energy:
#
#
# ```
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #########
#
# ```
#
# *What is the least energy required to organize the amphipods?*
###

test_input = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

test_output = 12521


class Node:
    def __init__(self, id) -> None:
        self.id = id


graph = {
    "h0": {"h1"},
    "h1": {"h0", "h2"},
    "h2": {"h1", "h3", "rA1"},
    "h3": {"h2", "h4"},
    "h4": {"h3", "h5", "rB1"},
    "h5": {"h4", "h6"},
    "h6": {"h5", "h7", "rC1"},
    "h7": {"h6", "h8"},
    "h8": {"h7", "h9", "rD1"},
    "h9": {"h8", "h10"},
    "h10": {"h9"},
    "rA1": {"rA2", "h2"},
    "rA2": {"rA1"},
    "rB1": {"rB2", "h4"},
    "rB2": {"rB1"},
    "rC1": {"rC2", "h6"},
    "rC2": {"rC1"},
    "rD1": {"rD2", "h8"},
    "rD2": {"rD1"},
}

PODS = ("A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2")
Conf = Tuple[str, str, str, str, str, str, str, str]


def solve(inp: TextIOWrapper):
    answer = None
    assert inp.readline().strip() == "#" * 13
    assert inp.readline().strip() == "#" + "." * 11 + "#"

    r1 = inp.readline().split("#")[3:7]
    r2 = inp.readline().split("#")[1:5]

    rooms = [list(z) for z in zip(r2, r1)]
    print(rooms)

    conf = [0] * 8
    sn = {"A": 0, "B": 0, "C": 0, "D": 0}
    for i, r1p in enumerate(r1):
        sn[r1p] += 1
        conf[pod_index(f"{r1p}{sn[r1p]}")] = f"r{chr(65+i)}1"
    for i, r2p in enumerate(r2):
        sn[r2p] += 1
        conf[pod_index(f"{r2p}{sn[r2p]}")] = f"r{chr(65+i)}2"

    conf = cast(Conf, tuple(conf))
    print(conf)

    return optimize(conf)


END_LETTERS = ("A", "A", "B", "B", "C", "C", "D", "D")


def is_end_conf(conf: Conf):
    """
    >>> is_end_conf(("rA1", "rA2", "rB1", "rB2", "rC1", "rC2", "rD1", "rD2"))
    True
    >>> is_end_conf(("rA2", "rA1", "rB1", "rB2", "rC2", "rC1", "rD1", "rD2"))
    True
    >>> is_end_conf(("rA2", "rA1", "rA1", "rB2", "rC2", "rC1", "rD1", "rD2"))
    False
    """
    for l, room in zip(END_LETTERS, conf):
        if not room[1] == l:
            return False
    return True


import heapq


def optimize(conf: Conf):
    if is_end_conf(conf):
        return 0

    shortest_paths: Dict[Tuple, Tuple[Optional[Conf], int]] = {conf: (None, 0)}
    visited: Set[Conf] = set()
    confs = [(0, conf)]
    heapq.heapify(confs)
    current_cost, current_node = heapq.heappop(confs)
    printed_max_cost = 0
    while not is_end_conf(current_node):
        visited.add(current_node)
        destinations = new_confs(current_node)
        weight_to_current = shortest_paths[current_node][1]
        if weight_to_current > printed_max_cost + 1000:
            printed_max_cost = weight_to_current
            print(weight_to_current, current_node)

        for next_cost, next_node in destinations:
            weight = next_cost + weight_to_current
            if next_node not in shortest_paths or shortest_paths[next_node][1] > weight:
                shortest_paths[next_node] = (current_node, weight)
                if next_node not in visited:
                    heapq.heappush(confs, (weight, next_node))

        assert len(confs) > 0
        current_cost, current_node = heapq.heappop(confs)
        # print(shortest_paths)

    return shortest_paths[current_node][1]


import functools


@functools.lru_cache(None)
def new_confs(conf: Conf) -> Sequence[Tuple[int, Conf]]:
    confs = []
    for pod, start_room in active_pods(conf):

        targets = paths(conf, pod, start_room)
        # print(pod, start_room, targets)

        for end_room, cost in targets:
            confs.append(
                (cost, tuple(end_room if p == pod else r for p, r in zip(PODS, conf)))
            )

    return confs


def settled_pod(pod: str, room: str, conf: Conf) -> bool:
    if room[0] != "r":
        return False
    if room[1] != pod[0]:
        return False
    if room[2] == "2":
        return True

    # Else, we're at rX1
    try:
        pod_blocked = conf.index(room[:2] + "2")
    except ValueError:
        return True
    return PODS[pod_blocked].startswith(pod[0])


def active_pods(conf: Conf) -> List[Tuple[str, str]]:
    return [
        (pod, room) for pod, room in zip(PODS, conf) if not settled_pod(pod, room, conf)
    ]


def paths(conf: Conf, pod, start_room):
    # print(pod, start_room)
    shortest_paths: Dict[str, Tuple[Optional[str], int]] = {start_room: (None, 0)}
    next_destinations = [start_room]

    while len(next_destinations) > 0:
        current_node = next_destinations.pop(0)
        destinations = graph[current_node]
        weight_to_current = shortest_paths[current_node][1]

        for next_node in destinations:
            if occupied(conf, next_node):
                continue
            weight = cost(pod) + weight_to_current
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
                next_destinations.append(next_node)

        # next node is the destination with the lowest weight
    return [
        (room, cost)
        for room, (prev, cost) in shortest_paths.items()
        if cost > 0 and valid_end_pos(conf, pod, room)
    ]


def pod_index(pod: str) -> int:
    return PODS.index(pod)


def valid_end_pos(conf: Conf, pod: str, room: str):
    pod_before = conf[pod_index(pod)]
    if room in ["h2", "h4", "h6", "h8"]:
        return False  # Hallway outside room
    if room[0] == "r" and room[1] != pod[0]:
        return False  # Foreign room
    if pod_before.startswith("h") and room.startswith("r") and room.endswith("1"):
        # Hallway to room with possible inhabitant
        other_comp = room[:2] + "2"
        if not occupied(conf, other_comp):
            return False  # Don't stop in room entrance if back is free
        return (
            PODS[conf.index(other_comp)][0] == pod[0]
        )  # Only enter if other occupant is same species
    if room.startswith("h") and pod_before.startswith("h"):
        return False  # Hallway to hallway
    return True


def occupied(conf: Conf, room):
    return room in conf


def cost(pod):
    if pod.startswith("A"):
        return 1
    elif pod.startswith("B"):
        return 10
    elif pod.startswith("C"):
        return 100
    else:
        assert pod.startswith("D")
        return 1000
