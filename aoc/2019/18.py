from collections import defaultdict
from dataclasses import dataclass
from io import TextIOBase, TextIOWrapper

test1 = (
    """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""",
    86,
)

test2 = (
    """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""",
    132,
)

test3 = (
    """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",
    136,
)
part1_test_input, part1_test_output = test3


@dataclass(frozen=True)
class Pos:
    x: int
    y: int
    obj: int

    def __repr__(self):
        return f"Pos(x={self.x}, y={self.y}, obj={chr(self.obj)})"


def neigh(map: list[list[str]], pos: Pos):
    r = [
        Pos(x=pos.x + 1, y=pos.y, obj=ord(map[pos.y][pos.x + 1])),
        Pos(x=pos.x - 1, y=pos.y, obj=ord(map[pos.y][pos.x - 1])),
        Pos(x=pos.x, y=pos.y + 1, obj=ord(map[pos.y + 1][pos.x])),
        Pos(x=pos.x, y=pos.y - 1, obj=ord(map[pos.y - 1][pos.x])),
    ]
    return [p for p in r if p.obj != ord("#")]


def simplify(
    map: list[list[str]], starts: list[Pos], keys: dict[int, Pos], all_doors: dict[int, Pos]
) -> dict[Pos, list[tuple[Pos, int, str]]]:
    visited: dict[Pos, set[Pos]] = defaultdict(set)
    queue = [(start, [start]) for start in starts]

    graph: dict[Pos, list[tuple[Pos, int, str]]] = defaultdict(list)
    while queue:
        node, path = queue.pop(0)
        visited[path[0]].add(node)
        for n in neigh(map, node):
            if len(path) > 1 and n == path[-2]:
                continue
            if n.obj in keys:
                doors = ""
                for i, prev in enumerate(reversed(path)):
                    if prev.obj in all_doors:
                        doors += chr(prev.obj)

                first = path[0]
                graph[first].append((n, i + 1, doors))
                # Add a new starting position
                queue.append((n, [n]))
                continue
            if n in visited[path[0]]:
                continue

            queue.append((n, path + [n]))
    return dict(graph)


@dataclass(frozen=True)
class State:
    pos: Pos
    keys: str


@dataclass(frozen=True)
class StateQuad:
    pos: tuple[Pos, ...]
    keys: str


def bfs(graph: dict[Pos, list[tuple[Pos, int, str]]], start: Pos, keys: dict[int, Pos]):
    visited: dict[State, int] = dict()
    queue = [(State(start, ""), [State(start, "")], 0)]
    max_keys = 0
    best = None
    while queue:
        state, path, old_dist = queue.pop(0)
        if state in visited and visited[state] <= old_dist:
            continue
        visited[state] = old_dist
        for n, dist, doors in graph[state.pos]:
            if any(door not in state.keys for door in doors.lower()):
                continue
            if n.obj != ord("@"):
                s = set(state.keys) | {chr(n.obj)}
                new_state = State(n, "".join(sorted(s)))
            else:
                new_state = State(n, state.keys)

            new_dist = old_dist + dist
            if new_state in visited and visited[new_state] <= new_dist:
                continue

            if n.obj != ord("@"):
                if len(new_state.keys) > max_keys:
                    max_keys = len(new_state.keys)
                    print(f"New record is {max_keys} keys")
                if len(new_state.keys) == len(keys):
                    if best is None or new_dist < best:
                        print("Found best path", new_dist)
                        best = new_dist
                    continue

            queue.append((new_state, path + [new_state], new_dist))
    return best


def bfs_quad(graph: dict[Pos, list[tuple[Pos, int, str]]], starts: tuple[Pos, Pos, Pos, Pos], keys: dict[int, Pos]):
    visited: dict[StateQuad, int] = dict()
    queue = [(StateQuad(starts, ""), [StateQuad(starts, "")], 0)]
    max_keys = 0
    best = None
    while queue:
        state, path, old_dist = queue.pop(0)
        if state in visited and visited[state] <= old_dist:
            continue
        visited[state] = old_dist
        for i, bot_pos in enumerate(state.pos):
            for n, dist, doors in graph[bot_pos]:
                if any(door not in state.keys for door in doors.lower()):
                    continue
                if n.obj != ord("@"):
                    s = set(state.keys) | {chr(n.obj)}
                    new_state = StateQuad(state.pos[:i] + (n,) + state.pos[i + 1 :], "".join(sorted(s)))
                else:
                    new_state = StateQuad(state.pos[:i] + (n,) + state.pos[i + 1 :], state.keys)

                new_dist = old_dist + dist
                if new_state in visited and visited[new_state] <= new_dist:
                    continue

                if n.obj != ord("@"):
                    if len(new_state.keys) > max_keys:
                        max_keys = len(new_state.keys)
                        print(f"New record is {max_keys} keys")
                    if len(new_state.keys) == len(keys):
                        if best is None or new_dist < best:
                            print("Found best path", new_dist)
                            best = new_dist
                        continue

                queue.append((new_state, path + [new_state], new_dist))
    return best


def part1(inp: TextIOWrapper):
    map, keys, doors, entrance = parse_map(inp)

    graph = simplify(map, [entrance], keys, doors)
    # pprint(graph)
    answer = bfs(graph, entrance, keys)

    return answer


part2_test_input = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############"""

part2_test_output = 32


def part2(inp: TextIOWrapper):
    map, keys, doors, entrance = parse_map(inp)

    x, y = entrance.x, entrance.y
    entrances = (
        Pos(x - 1, y - 1, entrance.obj),
        Pos(x + 1, y - 1, entrance.obj),
        Pos(x - 1, y + 1, entrance.obj),
        Pos(x + 1, y + 1, entrance.obj),
    )
    for e in entrances:
        map[e.y][e.x] = "@"
    map[y][x] = map[y - 1][x] = map[y + 1][x] = map[y][x - 1] = map[y][x + 1] = "#"

    graph = simplify(map, list(entrances), keys, doors)
    # pprint(graph)
    answer = bfs_quad(graph, entrances, keys)

    return answer


def parse_map(inp: TextIOBase):
    map = [list(l) for l in inp.readlines()]
    keys: dict[int, Pos] = {}
    doors: dict[int, Pos] = {}

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "@":
                entrance = Pos(x, y, ord(cell))
            elif "a" <= cell <= "z":
                keys[ord(cell)] = Pos(x, y, ord(cell))
            elif "A" <= cell <= "Z":
                doors[ord(cell)] = Pos(x, y, ord(cell))

    assert entrance
    return map, keys, doors, entrance
