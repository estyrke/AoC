from collections import defaultdict
from functools import cache
from io import StringIO, TextIOBase
import sys
from matplotlib import pyplot as plt
import networkx as nx


part1_test_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

part1_test_output = 2024


def part1(inp: TextIOBase):
    answer = None

    initial, gates = inp.read().split("\n\n")
    values = [k.split(": ") for k in initial.split("\n")]
    values = {k: int(v) for k, v in values}
    gates = [k.split() for k in gates.strip().split("\n")]
    gates = {g[4]: g[:3] for g in gates}
    print(values)
    print(gates)

    running = True
    while running:
        running = False
        for gate, (a_name, op, b_name) in gates.items():
            if gate in values:
                continue
            running = True
            a = values.get(a_name, None)
            b = values.get(b_name, None)
            if a is not None and b is not None:
                if op == "AND":
                    values[gate] = a & b
                elif op == "OR":
                    values[gate] = a | b
                elif op == "XOR":
                    values[gate] = a ^ b
                else:
                    assert False

    answer = 0
    for k, v in values.items():
        if k.startswith("z"):
            answer += v << int(k[1:])
    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    initial, gates = inp.read().split("\n\n")
    initial = [k.split(": ") for k in initial.split("\n")]
    initial = {k: int(v) for k, v in initial}
    gates = [k.split() for k in gates.strip().split("\n")]
    gates = {g[4]: g[:3] for g in gates}

    if IS_TEST:
        swaps = []
    else:
        swaps = [
            ("mvb", "z08"),
            ("jss", "rds"),
            ("z18", "wss"),
            ("z23", "bmn"),
        ]

    for a, b in swaps:
        gates[a], gates[b] = gates[b], gates[a]

    G = nx.DiGraph()
    for k, v in initial.items():
        G.add_node(k, label=k)
    for gate, (a, op, b) in gates.items():
        G.add_node(gate + op, label=f"{op}", op=op, gate=gate)
        G.add_node(gate, label=f"{gate}", op=op)
    for gate, (a, op, b) in gates.items():
        G.add_edge(a, gate + op)
        G.add_edge(b, gate + op)
        G.add_edge(gate + op, gate)

    deltas = defaultdict(int)

    @cache
    def get_pos(k: str):
        try:
            i = int(k[1:])
        except ValueError:
            i = None

        if k[0] == "x" and i is not None:
            return (-40 - (i) * 200, -50 + 0 * 25)
        if k[0] == "y" and i is not None:
            return (40 - i * 200, -50 + 0 * 25)
        if k[0] == "z" and i is not None:
            return (-i * 200, 100 + 0 * 25)
        for _, succ in nx.bfs_successors(G, k):
            for x in succ:
                if x[0] == "z" and x[1] in "0123456789":
                    new_pos = (
                        get_pos(x)[0] + deltas[x],
                        get_pos(x)[1] - nx.shortest_path_length(G, k, x) * 25 + deltas[x],
                    )

                    # To make sure nodes don't print on top of each other
                    deltas[new_pos] += 10
                    return new_pos[0] + deltas[new_pos], new_pos[1] + deltas[new_pos]

    pos = {k: get_pos(k) for k, v in G.nodes.items()}
    nx.draw(
        G,
        pos,
        node_size=200,
        font_size=10,
        labels={k: v["label"] for k, v in G.nodes.items()},
        with_labels=True,
    )
    plt.show()
    return ",".join(sorted([item for sublist in swaps for item in sublist]))


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
