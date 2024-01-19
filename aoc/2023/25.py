from collections import defaultdict
from io import StringIO, TextIOWrapper
from math import prod
import sys
from typing import cast
import networkx as nx

part1_test_input = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

part1_test_output = 54


def part1(inp: TextIOWrapper):
    graph: dict[str, set[str]] = defaultdict(set)
    edges: set[tuple[str, str]] = set()
    for line in inp.readlines():
        src, dsts = line.strip().split(": ")
        dsts = dsts.strip().split()
        graph[src] |= set(dsts)
        for dst in dsts:
            edges.add(cast(tuple[str, str], tuple(sorted([src, dst]))))
            graph[dst].add(src)

    G = nx.Graph(list(edges))

    pos = nx.spring_layout(G)

    def sort_f(edge: tuple[str, str]):
        s, e = edge
        s = pos[s]
        e = pos[e]
        return abs(s[0] - e[0]) ** 2 + abs(s[1] - e[1]) ** 2

    sorted_edges = sorted(edges, key=sort_f)
    new_edges = sorted_edges[:-3]
    G = nx.Graph(new_edges)
    return prod([len(sg) for sg in nx.connected_components(G)])


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = None

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
