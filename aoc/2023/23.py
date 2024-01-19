from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from io import StringIO, TextIOWrapper
import sys
from typing import Callable

part1_test_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

part1_test_output = 94


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def __repr__(self):
        return f"Pos(x={self.x}, y={self.y})"


def dfs(start: Pos, end: Pos, neigh: Callable[[Pos], dict[Pos, int]]):
    queue: list[tuple[Pos, set[Pos], int]] = [(start, set([start]), 0)]

    max_visited = {}
    i = 0
    while queue:
        node, visited, dist = queue.pop(0)
        if node == end:
            i += 1
            if i % 50000 == 0:
                print(datetime.now(), len(queue), i)
        # print(node, visited, dist)
        if node not in max_visited or dist > max_visited[node][1]:
            max_visited[node] = (visited, dist)

        for n, new_dist in neigh(node).items():
            assert n != node
            if n not in visited:
                queue.insert(0, (n, visited | set([n]), dist + new_dist))
    return max_visited[end]


def simplify(start: Pos, end: Pos, neigh: Callable[[Pos], list[Pos]]):
    queue: list[tuple[Pos, Pos, list[Pos], int]] = [
        (n, start, [start, n], 1) for n in neigh(start)
    ]
    # print(f"simplify start {start}: {queue}")
    # print("init_neigh", start, queue)
    neighs = dict()
    while queue:
        node, last_node, visited, dist = queue.pop(0)

        ns = [n for n in neigh(node) if n not in visited]

        if node == end:
            # print(f"simplify end {start} -> {end}: {dist}")
            if node not in neighs or neighs[node] < dist:
                neighs[node] = dist
            continue

        if len(ns) > 1:
            if node not in neighs or neighs[node] < dist:
                neighs[node] = dist
            continue
        for n in ns:
            queue.append((n, last_node, [*visited, n], dist + 1))

    return neighs


def part1(inp: TextIOWrapper):
    @lru_cache
    def neigh1(pos: Pos):
        r = [
            Pos(x=pos.x + 1, y=pos.y)
            if pos.x < len(lines[0]) - 1 and lines[pos.y][pos.x + 1] in ".>"
            else None,
            Pos(x=pos.x - 1, y=pos.y)
            if pos.x > 0 and lines[pos.y][pos.x - 1] in ".<"
            else None,
            Pos(x=pos.x, y=pos.y + 1)
            if pos.y < len(lines) - 1 and lines[pos.y + 1][pos.x] in ".v"
            else None,
            Pos(x=pos.x, y=pos.y - 1)
            if pos.y > 0 and lines[pos.y - 1][pos.x] in ".^"
            else None,
        ]
        return [p for p in r if p is not None]

    @lru_cache
    def neigh1_s(pos: Pos):
        return graph[pos]

    lines = [list(l.strip()) for l in inp.readlines()]

    graph = defaultdict(dict)

    start = Pos(1, 0)
    end = Pos(len(lines[-1]) - 2, len(lines) - 1)
    graph = dict()
    queue = [start]
    while queue:
        node = queue.pop(0)
        neighs = simplify(node, end, neigh1)
        # print(f"simplify {node} -> {neighs}")
        graph[node] = neighs
        for n, d in neighs.items():
            if n not in graph:
                queue.append(n)
    # pprint(graph)
    # for y, l in enumerate(lines):
    #    for x, c in enumerate(l):
    #        if Pos(x, y) in graph:
    #            print("*", end="")
    #        else:
    #            print(c, end="")
    #    print()
    path, length = dfs(
        Pos(1, 0),
        Pos(len(lines[-1]) - 2, len(lines) - 1),
        neigh1_s,
    )

    print(path, length)
    return length


part2_test_input = part1_test_input

part2_test_output = 154


def part2(inp: TextIOWrapper):
    @lru_cache
    def neigh2(pos: Pos):
        r = [
            Pos(x=pos.x + 1, y=pos.y)
            if pos.x < len(lines[0]) - 1 and lines[pos.y][pos.x + 1] != "#"
            else None,
            Pos(x=pos.x - 1, y=pos.y)
            if pos.x > 0 and lines[pos.y][pos.x - 1] != "#"
            else None,
            Pos(x=pos.x, y=pos.y + 1)
            if pos.y < len(lines) - 1 and lines[pos.y + 1][pos.x] != "#"
            else None,
            Pos(x=pos.x, y=pos.y - 1)
            if pos.y > 0 and lines[pos.y - 1][pos.x] != "#"
            else None,
        ]
        return [p for p in r if p is not None]

    lines = [list(l.strip()) for l in inp.readlines()]

    def neigh2_s(pos: Pos):
        return graph[pos]

    graph = defaultdict(dict)

    start = Pos(1, 0)
    end = Pos(len(lines[-1]) - 2, len(lines) - 1)
    graph = dict()
    queue = [start]
    while queue:
        node = queue.pop(0)
        neighs = simplify(node, end, neigh2)
        # print(f"simplify {node} -> {neighs}")
        graph[node] = neighs
        for n, d in neighs.items():
            if n not in graph:
                queue.append(n)
    import graphviz

    dot = graphviz.Digraph("23_map")

    for m, neigh in graph.items():
        dot.node(str(m), pos=f"{m.x},{-m.y}")

        for n, dist in neigh.items():
            dot.edge(str(m), str(n), str(dist))
    dot.render(engine="neato", view=True)

    path, length = dfs(
        Pos(1, 0),
        Pos(len(lines[-1]) - 2, len(lines) - 1),
        neigh2_s,
    )

    return length


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
