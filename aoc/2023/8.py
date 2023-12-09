from io import StringIO, TextIOWrapper
from math import lcm
import sys

part1_test_input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

part1_test_output = 6


def part1(inp: TextIOWrapper):
    lines = [l for l in inp.readlines()]
    moves = list(lines[0].strip())
    conn = lines[2:]
    conn = [l.split() for l in conn]
    conn = {p: (c1.strip("(),"), c2.strip("(),")) for p, _, c1, c2 in conn}

    node = "AAA"

    nmoves = 0
    while node != "ZZZ":
        move = moves[nmoves % len(moves)]
        assert move == "L" or move == "R"
        nmoves = nmoves + 1
        node = conn[node][0] if move == "L" else conn[node][1]

    return nmoves


part2_test_input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

part2_test_output = 6


def part2(inp: TextIOWrapper):
    lines = [l for l in inp.readlines()]
    moves = list(lines[0].strip())
    conn = lines[2:]
    conn = [l.split() for l in conn]
    conn = {p: (c1.strip("(),"), c2.strip("(),")) for p, _, c1, c2 in conn}

    start_nodes = [n for n in conn.keys() if n.endswith("A")]

    lens = []
    for start_node in start_nodes:
        nmoves = 0
        node = start_node
        while not node.endswith("Z"):
            move = moves[nmoves % len(moves)]
            assert move == "L" or move == "R"
            nmoves = nmoves + 1
            dir = 0 if move == "L" else 1
            node = conn[node][dir]

        lens.append(nmoves)

    return lcm(*lens)


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
