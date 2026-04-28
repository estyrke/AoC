from networkx.classes.digraph import DiGraph
from collections import defaultdict
from io import StringIO, TextIOBase
import sys
import networkx as nx

part1_test_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

part1_test_output = 5


def dfs(conns: dict[str, list[str]], src: str, target: str, mid: set[str]):
    q = [(src, set([src]))]
    seen = set()
    out = []
    while q:
        state, path = q.pop(0)

        if state == target:
            if path.issuperset(mid):
                #print(path)
                out.append(path)
            #else:

            continue
        for new_state in conns[state]:
            assert new_state not in path
            q.insert(0, (new_state, path | set([new_state])))
    return out

def part1(inp: TextIOBase):
    answer = None


    lines = [l.strip().split() for l in inp.readlines()]
    conns = {c[0].removesuffix(":"): c[1:] for c in lines}


        # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return len(dfs(conns, "you", "out", set()))


part2_test_input = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

part2_test_output = 2



def dfs2(conns: dict[str, list[str]], src: str, target: str):
    q = [(src, [src])]
    seen = set()
    out = []
    while q:
        state, path = q.pop(0)

        if state == target:
            #print(len(path))
            out.append(path)

            continue
        for new_state in conns.get(state, []):
            assert new_state not in path
            q.insert(0, (new_state, path+[new_state]))
    return out
def part2(inp: TextIOBase):
    lines = [l.strip().split() for l in inp.readlines()]
    conns = {c[0].removesuffix(":"): c[1:] for c in lines}

    g = DiGraph(conns)
    print(g)
    print([x for x in g.nodes() if g.out_degree(x)==0]
)
    answer = 1
    answer *= (len(list(nx.all_simple_paths(g, "dac", "out"))))
    print(answer)

    prune = ["out"]
    while prune:
        g.remove_nodes_from(prune)
        prune = [x for x in g.nodes() if g.out_degree(x)==0 and x != "dac"]
        print(prune)

    answer *= (len(list(nx.all_simple_paths(g, "fft", "dac"))))
    print(answer)

    prune = ["dac"]
    while prune:
        g.remove_nodes_from(prune)
        prune = [x for x in g.nodes() if g.out_degree(x)==0 and x != "fft"]
        print(prune)

    answer *= len(list(nx.all_simple_paths(g, "svr", "fft")))
    print(answer)
    g.reverse
    return answer
    rev_conns = defaultdict(list)
    for s, e in conns.items():
        for new_s in e:
            rev_conns[new_s].append(s)
    #paths = bfs(conns, "svr", "out", {"fft", "dac"})
    print("a")
    ffts = dfs2(rev_conns, "fft", target= "svr")
    print("b", ffts)
    keep = set()
    for i, fft in enumerate(ffts):
        keep |= set(fft)
        #for j in range(1, len(fft)):
        #    keep[fft[j]] = fft[j-1]


    print(keep)
    q = ["svr"]
    print("conns", conns)
    while q:
        curr = q.pop()
        if curr == "fft" or curr == "dac" or curr == "out":
            continue
        q.extend(conns.get(curr, []))
        if curr not in keep and curr in conns:
            print("prune", curr)
            del conns[curr]
    print("conns", conns)

    for s in conns:
        conns[s] = [conn for conn in conns.get(s, []) if conn in conns]

    print("conns", conns)
    return None


    dacs = dfs2(conns, "fft", "dac")
    print("c", dacs)
    outs = dfs2(conns, "dac", "out")
    print("d", outs)
    #ffts = dfs2(conns, "svr", "fft", set())
    #dacs = dfs2(conns, "svr", "dac", set())

    return len(ffts) * len(dacs) * len(outs) + 1


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
