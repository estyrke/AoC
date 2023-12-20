from collections import defaultdict
from io import StringIO, TextIOWrapper
from math import lcm
import sys

part1_test_input = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

part1_test_input = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

part1_test_output = 32000000
part1_test_output = 11687500


class Broadcast:
    def __init__(self, dst: list[str]):
        self.name = "broadcaster"
        self.dst = [d.strip() for d in dst]

    def low(self, src: str):
        return [(self.name, dst, False) for dst in self.dst]

    def high(self, src: str):
        return [(self.name, dst, True) for dst in self.dst]


class FlipFlop:
    def __init__(self, name: str, dst: list[str]):
        self.name = name
        self.dst = [d.strip() for d in dst]
        self.state = False

    def low(self, src: str):
        self.state = not self.state
        return [(self.name, dst, self.state) for dst in self.dst]

    def high(self, src: str):
        return []


class Conjunction:
    def __init__(self, name: str, dst: list[str]):
        self.name = name
        self.dst = [d.strip() for d in dst]
        self.mem = {}

    def low(self, src: str):
        self.mem[src] = False
        return [(self.name, dst, True) for dst in self.dst]

    def high(self, src: str):
        self.mem[src] = True

        sig = not all(self.mem.values())
        return [(self.name, dst, sig) for dst in self.dst]


def part1(inp: TextIOWrapper):
    lines = [l for l in inp.readlines()]
    modules = {}
    srcs = defaultdict(list)
    for l in lines:
        if l.startswith("broadcaster"):
            dsts = [d.strip() for d in l.split(" -> ")[1].strip().split(",")]
            modules["broadcaster"] = Broadcast(dsts)
            [srcs[dst].append("broadcaster") for dst in dsts]
        elif l.startswith("%"):
            name, dsts = l[1:].split(" -> ", 2)
            dsts = [d.strip() for d in dsts.split(",")]

            modules[name] = FlipFlop(name, dsts)
            [srcs[dst].append(name) for dst in dsts]
        elif l.startswith("&"):
            name, dsts = l[1:].split(" -> ", 2)
            dsts = [d.strip() for d in dsts.split(",")]
            modules[name] = Conjunction(name, dsts)
            [srcs[dst].append(name) for dst in dsts]
        else:
            assert False

    for m in modules.values():
        if isinstance(m, Conjunction):
            m.mem = {s: False for s in srcs[m.name]}
            print(m.name, m.mem)

    low = 0
    high = 0
    for i in range(1000):
        pulses: list[tuple[str, str, bool]] = [("button", "broadcast", False)]
        low += 1
        while pulses:
            src, dst, sig = pulses.pop(0)
            if dst not in modules:
                # print(dst)
                continue
            if sig:
                new_sigs = modules[dst].high(src)
            else:
                new_sigs = modules[dst].low(src)
            new_low = len([x for x in new_sigs if not x[2]])
            low += new_low
            high += len(new_sigs) - new_low
            pulses.extend(new_sigs)

    print(low, high)
    return low * high


part2_test_input = None

part2_test_output = None


def part2(inp: TextIOWrapper):
    lines = [l for l in inp.readlines()]
    modules = {}
    srcs: defaultdict[str, list[str]] = defaultdict(list)
    for l in lines:
        if l.startswith("broadcaster"):
            dsts = [d.strip() for d in l.split(" -> ")[1].strip().split(",")]
            modules["broadcaster"] = Broadcast(dsts)
            [srcs[dst].append("broadcaster") for dst in dsts]
        elif l.startswith("%"):
            name, dsts = l[1:].split(" -> ", 2)
            dsts = [d.strip() for d in dsts.split(",")]

            modules[name] = FlipFlop(name, dsts)
            [srcs[dst].append(name) for dst in dsts]
        elif l.startswith("&"):
            name, dsts = l[1:].split(" -> ", 2)
            dsts = [d.strip() for d in dsts.split(",")]
            modules[name] = Conjunction(name, dsts)
            [srcs[dst].append(name) for dst in dsts]
        else:
            assert False

    import graphviz

    dot = graphviz.Digraph("machine")

    for m in modules.values():
        dot.node(m.name, f"{m.name} {m.__class__.__name__[:3]}")
    for dst, ss in srcs.items():
        [dot.edge(src, dst) for src in ss]
    dot.render(directory="doctest-output", view=True)

    for m in modules.values():
        if isinstance(m, Conjunction):
            m.mem = {s: False for s in srcs[m.name]}
            print(m.name, m.mem)

    # There is a conjunction connected to the final ouput (rx) - find it
    target_signal = "rx"
    assert len(srcs[target_signal]) == 1
    final_conj = srcs[target_signal][0]

    print(f"final_conj '{final_conj}'")
    # Find the cycles where this conj's inputs change
    cycles = calc_cycle(modules, final_conj)

    # find the length of cycles for the inputs by taking the difference between consecutive triggers
    for n in cycles.keys():
        print(f"{n} diff", [x - y for x, y in zip(cycles[n][1:], cycles[n])])
    diffs = [k[1] - k[0] for k in cycles.values()]

    # The answer is the lowest common multiplier of these inputs
    # i.e. when they all align the final conjunction will trigger.
    print("final_conj cycle ->", answer := lcm(*diffs))

    return answer


def calc_cycle(modules, target: str):
    sel = dict(modules[target].mem)
    ans2 = {k: list() for k in sel.keys()}
    i = 0
    while not all([len(v) >= 2 for v in ans2.values()]):
        i += 1
        pulses: list[tuple[str, str, bool]] = [("button", "broadcaster", False)]

        while pulses:
            src, dst, sig = pulses.pop(0)
            if dst not in modules:
                continue
            if sig:
                new_sigs = modules[dst].high(src)
            else:
                new_sigs = modules[dst].low(src)

            if dst == target:
                for k in sel.keys():
                    if sel[k] is False and modules[target].mem[k] is True:
                        ans2[k].append(i)
                sel = dict(modules[target].mem)
            pulses.extend(new_sigs)

    return ans2


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
