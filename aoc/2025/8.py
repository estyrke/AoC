from _operator import mul
from _operator import add
from functools import reduce
from math import sqrt
from io import StringIO, TextIOBase
import sys
import networkx as nx

part1_test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

part1_test_output = 40


def part1(inp: TextIOBase):
    answer = None

    boxes = []
    dists = []
    graph = {}
    for i, line in enumerate(inp.readlines()):
        box = line.strip().split(",")
        x, y, z = [int(c ) for c in box]
        for j, (x2, y2, z2) in enumerate(boxes):
            dists.append((sqrt((x-x2)**2+(y-y2)**2+(z-z2)**2), j, len(boxes)))
        boxes.append((x, y, z))

    if IS_TEST:
        num_conn = 10
    else:
        num_conn=1000
    dists = sorted(dists)[:num_conn]
    graph = nx.Graph([(i, j) for d, i, j in dists])

    answer = reduce(mul, [len(c) for c in sorted(nx.connected_components(graph), key=len, reverse=True)][:3], 1)

    return answer


part2_test_input = part1_test_input

part2_test_output = 25272


def part2(inp: TextIOBase):

    boxes = []
    dists = []
    graph = {}
    for i, line in enumerate(inp.readlines()):
        box = line.strip().split(",")
        x, y, z = [int(c ) for c in box]
        for j, (x2, y2, z2) in enumerate(boxes):
            dists.append((sqrt((x-x2)**2+(y-y2)**2+(z-z2)**2), j, len(boxes)))
        boxes.append((x, y, z))

    dists.sort()
    graph = nx.Graph()
    graph.add_nodes_from(boxes)
    for d, i, j in dists:
        graph.add_edge(boxes[i], boxes[j])
        if nx.components.is_connected(graph):
            return boxes[i][0] * boxes[j][0]


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
