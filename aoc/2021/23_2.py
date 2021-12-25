from io import TextIOWrapper
import math
from typing import Dict, Generator, List, Optional, Sequence, Set, Tuple, Union, cast
import functools

###
# ## --- Part Two ---
#
# As you prepare to give the amphipods your solution, you notice that
# the diagram they handed you was actually folded up. As you unfold it,
# you discover an extra part of the diagram.
#
# Between the first and second lines of text that contain amphipod
# starting positions, insert the following lines:
#
#
# ```
#   #D#C#B#A#
#   #D#B#A#C#
#
# ```
#
# So, the above example now becomes:
#
#
# ```
# #############
# #...........#
# ###B#C#B#D###
#   *#D#C#B#A#
#  #D#B#A#C#*
#   #A#D#C#A#
#   #########
#
# ```
#
# The amphipods still want to be organized into rooms similar to before:
#
#
# ```
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# ```
#
# In this updated example, the least energy required to organize these
# amphipods is `*44169*`:
#
#
# ```
# #############
# #...........#
# ###B#C#B#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #..........D#
# ###B#C#B#.###
#   #D#C#B#A#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A.........D#
# ###B#C#B#.###
#   #D#C#B#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A........BD#
# ###B#C#.#.###
#   #D#C#B#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #A......B.BD#
# ###B#C#.#.###
#   #D#C#.#.#
#   #D#B#A#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#C#.#.###
#   #D#C#.#.#
#   #D#B#.#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#.#.#.###
#   #D#C#.#.#
#   #D#B#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.....B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#B#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA...B.B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#D#C#A#
#   #########
#
# #############
# #AA.D.B.B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#.#C#A#
#   #########
#
# #############
# #AA.D...B.BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#.#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D.....BD#
# ###B#.#.#.###
#   #D#.#C#.#
#   #D#B#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D......D#
# ###B#.#.#.###
#   #D#B#C#.#
#   #D#B#C#C#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D......D#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#A#
#   #########
#
# #############
# #AA.D.....AD#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#.#
#   #########
#
# #############
# #AA.......AD#
# ###B#.#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.......AD#
# ###.#B#C#.###
#   #D#B#C#.#
#   #D#B#C#.#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.......AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #D#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #AA.D.....AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #.#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #A..D.....AD#
# ###.#B#C#.###
#   #.#B#C#.#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #...D.....AD#
# ###.#B#C#.###
#   #A#B#C#.#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #.........AD#
# ###.#B#C#.###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #..........D#
# ###A#B#C#.###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #A#B#C#D#
#   #A#B#C#D#
#   #########
#
# ```
#
# Using the initial configuration from the full diagram, *what is the
# least energy required to organize the amphipods?*
###B#C#B#D###
# A#D#C#A#
#########"""

test_output = 44169


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
    "rA2": {"rA1", "rA3"},
    "rA3": {"rA2", "rA4"},
    "rA4": {"rA3"},
    "rB1": {"rB2", "h4"},
    "rB2": {"rB1", "rB3"},
    "rB3": {"rB2", "rB4"},
    "rB4": {"rB3"},
    "rC1": {"rC2", "h6"},
    "rC2": {"rC1", "rC3"},
    "rC3": {"rC2", "rC4"},
    "rC4": {"rC3"},
    "rD1": {"rD2", "h8"},
    "rD2": {"rD1", "rD3"},
    "rD3": {"rD2", "rD4"},
    "rD4": {"rD3"},
}

Conf = Tuple[
    str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str
]

Hallway = Tuple[
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
    Optional[str],
]
Room = Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
Conf = Tuple[Hallway, Room, Room, Room, Room]


def solve(inp: TextIOWrapper):
    assert inp.readline().strip() == "#" * 13
    assert inp.readline().strip() == "#" + "." * 11 + "#"

    r1 = inp.readline().split("#")[3:7]
    # D#C#B#A#
    # D#B#A#C#
    r2 = ["D", "C", "B", "A"]
    r3 = ["D", "B", "A", "C"]
    r4 = inp.readline().split("#")[1:5]

    rooms = [reversed(list(z)) for z in zip(r4, r3, r2, r1)]

    conf: Conf = (
        (None, None, None, None, None, None, None),
        cast(Room, tuple(rooms[0])),
        cast(Room, tuple(rooms[1])),
        cast(Room, tuple(rooms[2])),
        cast(Room, tuple(rooms[3])),
    )

    print(conf)

    # return None
    return optimize(conf)


END_LETTERS = (
    "A",
    "B",
    "C",
    "D",
)


def is_end_conf(conf: Conf):
    """
    >>> is_end_conf(((None, None, None, None, None, None, None), ("A", "A", "A", "A"), ("B", "B", "B", "B"), ("C", "C", "C", "C"), ("D", "D", "D", "D")))
    True
    >>> is_end_conf((("A", None, None, None, None, None, None), (None, "A", "A", "A"), ("B", "B", "B", "B"), ("C", "C", "C", "C"), ("D", "D", "D", "D")))
    False
    >>> is_end_conf(((None, None, None, None, None, None, None), ("B", "A", "A", "A"), ("A", "B", "B", "B"), ("C", "C", "C", "C"), ("D", "D", "D", "D")))
    False
    """
    if any(p is not None for p in conf[0]):
        return False

    for l, room in zip(END_LETTERS, conf[1:]):
        if any(p != l for p in room):
            return False
    return True


b = 0


@functools.lru_cache(None)
def optimize(conf: Conf):
    if is_end_conf(conf):
        return 0

    destinations = new_confs(conf)

    if False and len(destinations) == 0:
        global b
        b += 1
        print("blocked", conf)
        if b > 20:
            raise RuntimeError()
        return None
    cost = None
    for next_cost, next_conf in destinations:
        c = optimize(next_conf)
        if c is None:
            continue
        new_cost = next_cost + c
        if cost is None or new_cost < cost:
            cost = new_cost

    return cost


# @functools.lru_cache(None)
def new_confs(conf: Conf) -> Sequence[Tuple[int, Conf]]:
    confs = []
    # print(conf)
    # print(list(active_start_rooms(conf)))
    for start_room, pod in active_start_rooms(conf):

        targets = paths(conf, pod, start_room)
        # print(pod, start_room, targets)

        for end_room, cost in targets:
            new_hallway = tuple(
                (
                    None
                    if start_room == hallway_name(hi)
                    else (pod if end_room == hallway_name(hi) else h)
                )
                for hi, h in enumerate(conf[0])
            )

            new_room1 = tuple(
                (
                    None
                    if start_room == room_name(0, ri)
                    else (pod if end_room == room_name(0, ri) else r)
                )
                for ri, r in enumerate(conf[1])
            )
            new_room2 = tuple(
                (
                    None
                    if start_room == room_name(1, ri)
                    else (pod if end_room == room_name(1, ri) else r)
                )
                for ri, r in enumerate(conf[2])
            )
            new_room3 = tuple(
                (
                    None
                    if start_room == room_name(2, ri)
                    else (pod if end_room == room_name(2, ri) else r)
                )
                for ri, r in enumerate(conf[3])
            )
            new_room4 = tuple(
                (
                    None
                    if start_room == room_name(3, ri)
                    else (pod if end_room == room_name(3, ri) else r)
                )
                for ri, r in enumerate(conf[4])
            )
            confs.append(
                (cost, (new_hallway, new_room1, new_room2, new_room3, new_room4))
            )

    # print(confs)
    # return "F"
    return confs


def hallway_name(index: int) -> str:
    """
    >>> hallway_name(0)
    'h0'
    >>> hallway_name(1)
    'h1'
    >>> hallway_name(2)
    'h3'
    >>> hallway_name(3)
    'h5'
    >>> hallway_name(4)
    'h7'
    >>> hallway_name(5)
    'h9'
    >>> hallway_name(6)
    'h10'
    """
    if index < 2:
        return f"h{index}"
    elif index < 3:
        return f"h{index+1}"
    elif index < 4:
        return f"h{index+2}"
    elif index < 5:
        return f"h{index+3}"
    else:
        return f"h{index+4}"


def hallway_index(h: str) -> Optional[int]:
    """
    >>> hallway_index('h0')
    0
    >>> hallway_index('h1')
    1
    >>> hallway_index('h3')
    2
    >>> hallway_index('h5')
    3
    >>> hallway_index('h7')
    4
    >>> hallway_index('h9')
    5
    >>> hallway_index('h10')
    6
    >>> hallway_index('h2')
    """
    index = int(h[1:])
    if index < 2:
        return index
    elif index == 3:
        return 2
    elif index == 5:
        return 3
    elif index == 7:
        return 4
    elif index >= 9:
        return index - 4

    return None


def room_name(room_index, position_index):
    """
    >>> room_name(0, 0)
    'rA1'
    """
    return f"r{pod_name(room_index)}{position_index+1}"


def room_index(name: str) -> int:
    assert name[1] in ["A", "B", "C", "D"]
    return pod_index(name[1])


def room_or_hallway_index(name: str) -> int:
    if name[0] == "h":
        return 0
    return room_index(name) + 1


def room_position(name: str) -> int:
    return int(name[2]) - 1


def active_start_rooms(conf: Conf) -> Generator[Tuple[str, str], None, None]:
    for i, hallway_inhabitant in enumerate(conf[0]):
        if hallway_inhabitant is not None:
            yield hallway_name(i), hallway_inhabitant
    for ri, room in enumerate(conf[1:]):
        native = pod_name(ri)
        if any(inh is not None and inh != native for inh in room):
            for ii, room_inhabitant in enumerate(room):
                if room_inhabitant is not None:
                    yield room_name(ri, ii), room_inhabitant
                    break


def paths(conf: Conf, pod, start_room):
    """
    >>> paths(((None, None, None, None, None, None, None), ('D', 'D', 'D', 'C'), ('B', 'C', 'B', 'A'), ('A', 'B', 'A', 'D'), ('C', 'A', 'C', 'B')), "D", "rA1")
    [('h3', 2000), ('h1', 2000), ('h0', 3000), ('h5', 4000), ('h7', 6000), ('h9', 8000), ('h10', 9000)]
    """
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
        if cost > 0
        and valid_end_pos(conf[room_or_hallway_index(room)], pod, start_room, room)
    ]


def pod_index(pod: str) -> int:
    """
    >>> pod_index("A")
    0
    """
    return ord(pod) - 65


def pod_name(pod_index: int) -> str:
    """
    >>> pod_name(3)
    'D'
    """
    return chr(65 + pod_index)


@functools.lru_cache(None)
def valid_end_pos(
    end_room: Union[Room, Hallway], pod: str, room_before: str, room: str
):
    """
    >>> conf = (('A', 'B', 'B', 'C', 'D', 'C', 'A'), (None, 'D', 'D', 'C'), (None, None, 'B', 'A'), (None, None, 'A', 'D'), (None, None, 'C', 'B'))
    >>> valid_end_pos((None, None, None, None), "A", "rB1", "rA4")
    True
    >>> valid_end_pos((None, None, None, None), "A", "rB1", "rA3")
    False
    >>> valid_end_pos((None, None, None, "A"), "A", "rB1", "rA3")
    True
    >>> valid_end_pos((None, None, None, "A"), "A", "rB1", "rA2")
    False
    >>> valid_end_pos((None, None, None, "B"), "A", "rB1", "rA3")
    False
    """
    if room in ["h2", "h4", "h6", "h8"]:
        return False  # Hallway outside room
    if room.startswith("h"):
        return not room_before.startswith(
            "h"
        )  # Hallway from hallway is not ok, but hallway from room is
    if room[0] == "r":
        if room[1] != pod:
            return False  # Foreign room
        if room_before[:2] == room[:2]:
            return False  # Same room
        native = pod_name(room_index(room))
        if any(r is not None and r != native for r in end_room):
            # Foreign inhabitants in my room
            return False
        # Hallway to room with possible inhabitant
        for inner in range(3, -1, -1):
            inner_comp = room[:2] + str(inner + 1)
            if end_room[inner] is None:
                return inner_comp == room  # First free room
            elif inner_comp == room:
                return False

    print(end_room, pod, room_before, room)
    assert False
    return True


def occupied(conf: Conf, room: str) -> bool:

    if room.startswith("h"):
        i = hallway_index(room)
        if i is None:
            return False
        return conf[0][i] is not None

    return conf[1 + room_index(room)][room_position(room)] is not None


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
