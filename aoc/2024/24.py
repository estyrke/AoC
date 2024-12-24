from io import StringIO, TextIOBase
import itertools
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
        for gate, (a, op, b) in gates.items():
            if gate in values:
                continue
            running = True
            a = values.get(a, None)
            b = values.get(b, None)
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
    answer = None

    initial, gates = inp.read().split("\n\n")
    initial = [k.split(": ") for k in initial.split("\n")]
    initial = {k: int(v) for k, v in initial}
    gates = [k.split() for k in gates.strip().split("\n")]
    gates = {g[4]: g[:3] for g in gates}
    # print(initial)
    # print(gates)

    G = nx.DiGraph()
    for k, v in initial.items():
        G.add_node(k, label=k)
    for gate, (a, op, b) in gates.items():
        G.add_node(gate, label=f"{op} {gate}")
        G.add_edge(a, gate)
        G.add_edge(b, gate)

    # nx.draw_shell(G, with_labels=True)
    # plt.show()

    x = y = 0
    x_size = y_size = z_size = 0
    for k, v in initial.items():
        if k.startswith("x"):
            x += v << int(k[1:])
            G.nodes[k]["depth"] = 0
            for n, succ in nx.bfs_successors(G, k):
                for s in succ:
                    G.nodes[s]["depth"] = G.nodes[n]["depth"] + 1
            x_size += 1
        if k.startswith("y"):
            y += v << int(k[1:])
            G.nodes[k]["depth"] = 0
            G.nodes[k]["depth"] = 0
            for n, succ in nx.bfs_successors(G, k):
                for s in succ:
                    # if G.nodes[s].get("depth", G.nodes[n]["depth"] + 1) != G.nodes[n]["depth"] + 1:
                    #    raise RuntimeError(
                    #        f"Node {s} has depth {G.nodes[s].get('depth', 0)} != {G.nodes[n]['depth'] + 1}"
                    #    )
                    G.nodes[s]["depth"] = G.nodes[n]["depth"] + 1
            y_size += 1
    for k in gates.keys():
        if k.startswith("z"):
            z_size += 1

    z = calc(gates, x, y)
    print(z, x_size, y_size, z_size)

    # print_subgraph(gates, "z01")
    if not IS_TEST:
        for z in range(z_size):
            G_sub = nx.subgraph(G, nx.ancestors(G, f"z{z:02}") | {f"z{z:02}"})

            # pos: dict = nx.spring_layout(G_sub, iterations=100)
            pos = nx.multipartite_layout(G, subset_key="depth")
            # for node in pos:
            # level = G_sub.nodes[node]["depth"]
            # pos[node] += (0, 10 * level)
            plt.figure()
            nx.draw(G_sub, pos, labels={k: v["label"] for k, v in G_sub.nodes.items()}, with_labels=True)
        plt.show()

    if IS_TEST:
        swaps = []
    else:
        swaps = [
            # ("pbm", "djm"),
        ]

    for a, b in swaps:
        gates[a], gates[b] = gates[b], gates[a]

    candidates = []
    for i in range(z_size):
        new_candidates = check_bit(i, gates)
        if new_candidates is not None:
            candidates.append(new_candidates)
            print(len(new_candidates))
        else:
            print("Bit %d is OK" % i)

    for i, cl1 in enumerate(candidates):
        # print(len(cl1), len(cl2))
        # print(len(cl1 & cl2))
        print(f"Trying {i}")
        for j, cl2 in enumerate(candidates[i:]):
            # print(f"Against {i+j}")
            for c1, c2 in itertools.combinations(cl1 & cl2, 2):
                new_gates = gates.copy()
                new_gates[c1], new_gates[c2] = new_gates[c2], new_gates[c1]

                if check_bit(i, new_gates) is None:
                    print("Success, when swapped", c1, c2)


def check_bit(i, gates):
    if calc(gates, 1 << i, 0) is None:
        # print("Loop detected")
        return outputs_subgraph(gates, f"z{i:02}")
    if calc(gates, 1 << i, 0) >> i & 1 != 1:
        # print("Fault at bit %d (1 + 0 != 1)" % i)
        # print_subgraph(gates, f"z{i:02}")
        return outputs_subgraph(gates, f"z{i:02}")
    if calc(gates, 1 << i, 1 << i) >> i & 2 != 2:
        # print(f"Fault at bit {i} (1 + 1 == {calc(gates, 1 << i, 1 << i) >> i & 2})")
        # print_subgraph(gates, f"z{i:02}")
        return outputs_subgraph(gates, f"z{i:02}")
    if calc(gates, 0, 1 << i) >> i & 1 != 1:
        # print("Fault at bit %d (0 + 1 != 1)" % i)
        # print_subgraph(gates, f"z{i:02}")
        return outputs_subgraph(gates, f"z{i:02}")
    if calc(gates, 0, 0) >> i & 1 != 0:
        # print("Fault at bit %d (0 + 0 != 0)" % i)
        # print_subgraph(gates, f"z{i:02}")
        return outputs_subgraph(gates, f"z{i:02}")
    # print("Bit %d is OK" % i)
    return None


def print_subgraph(gates, initial: str):
    queue = [initial]
    G = nx.DiGraph()
    path = []
    while queue:
        node = queue.pop(0)
        a, op, b = gates[node]
        path.append(f"{a} {op} {b} -> {node}")
        G.add_edge(a, node, label=op)
        G.add_edge(b, node, label=op)
        if not a.startswith("x") and not a.startswith("y"):
            queue.append(a)
        if not b.startswith("x") and not b.startswith("y"):
            queue.append(b)

    print("\n".join(reversed(path)))


def outputs_subgraph(gates, initial: str):
    queue = [initial]
    path = set()
    while queue:
        node = queue.pop(0)
        a, op, b = gates[node]
        if node in path:
            return None
        path.add(node)
        if not a.startswith("x") and not a.startswith("y"):
            queue.append(a)
        if not b.startswith("x") and not b.startswith("y"):
            queue.append(b)

    return path


def calc(gates, x: int, y: int) -> int | None:
    running = True
    values = {}
    for k, (a, op, b) in gates.items():
        if a.startswith("x"):
            values[a] = x >> int(a[1:]) & 1
        if b.startswith("x"):
            values[b] = x >> int(b[1:]) & 1
        if a.startswith("y"):
            values[a] = y >> int(a[1:]) & 1
        if b.startswith("y"):
            values[b] = y >> int(b[1:]) & 1
    visited = set()
    z_gates = set()
    while running:
        running = False
        for gate, (a, op, b) in gates.items():
            if gate.startswith("z"):
                z_gates.add(gate)
            if gate in visited:
                return None
            visited.add(gate)
            if gate in values:
                continue
            a = values.get(a, None)
            b = values.get(b, None)
            if a is not None and b is not None:
                if op == "AND":
                    running = True
                    values[gate] = a & b
                elif op == "OR":
                    running = True
                    values[gate] = a | b
                elif op == "XOR":
                    running = True
                    values[gate] = a ^ b
                else:
                    assert False
    res = 0
    for k, v in values.items():
        if k.startswith("z"):
            z_gates.remove(k)
            res += v << int(k[1:])

    assert not z_gates
    return res


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
