from io import StringIO, TextIOBase
import itertools
import sys
import networkx as nx

part1_test_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

part1_test_output = 7


def part1(inp: TextIOBase):
    answer = None

    G = nx.Graph()
    for line in inp.readlines():
        a, b = line.strip().split("-")
        G.add_edge(a, b)

    answer = 0
    for n1, n2, n3 in itertools.combinations(G.nodes, 3):
        if n2 in G.neighbors(n1) and n3 in G.neighbors(n1) and n3 in G.neighbors(n2):
            if n1.startswith("t") or n2.startswith("t") or n3.startswith("t"):
                answer += 1
    return answer


part2_test_input = part1_test_input

part2_test_output = "co,de,ka,ta"


def part2(inp: TextIOBase):
    G = nx.Graph()
    for line in inp.readlines():
        a, b = line.strip().split("-")
        G.add_edge(a, b)

    lan = nx.clique.max_weight_clique(G, weight=None)
    return ",".join(sorted(lan[0]))


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
