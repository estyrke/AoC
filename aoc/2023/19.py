from collections import defaultdict
from io import StringIO, TextIOWrapper
from math import prod
import sys

part1_test_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

part1_test_output = 19114


def part1(inp: TextIOWrapper):
    answer = 0

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]
    workflows, parts = inp.read().split("\n\n")
    workflows = {
        w.strip().split("{")[0]: w.strip().split("{")[1] for w in workflows.splitlines()
    }
    workflows = {n: rs.strip("{}").split(",") for n, rs in workflows.items()}
    print(workflows)
    for part in parts.splitlines():
        ns = {
            "xmas"[i]: int(n.split("=")[1])
            for i, n in enumerate(part.strip("{}").split(","))
        }
        next_wf = "in"
        while next_wf not in ["A", "R"]:
            wf = workflows[next_wf]
            for step in wf:
                if ":" not in step:
                    next_wf = step
                    break
                cond, nw = step.split(":")
                if eval(cond, {}, ns) is True:
                    next_wf = nw
                    break
                else:
                    continue
        if next_wf == "A":
            print("Accepted", ns)
            answer += sum(ns.values())

    return answer


part2_test_input = part1_test_input

part2_test_output = 167409079868000


def part2(inp: TextIOWrapper):
    workflows, parts = inp.read().split("\n\n")
    workflows = {
        w.strip().split("{")[0]: w.strip().split("{")[1] for w in workflows.splitlines()
    }
    workflows = {n: rs.strip("{}").split(",") for n, rs in workflows.items()}

    targets = defaultdict(list)
    queue: list[tuple[str, dict[str, set[int]]]] = [
        (
            "in",
            {
                "x": set(range(1, 4001)),
                "m": set(range(1, 4001)),
                "a": set(range(1, 4001)),
                "s": set(range(1, 4001)),
            },
        )
    ]
    while queue:
        next_wf, ranges = queue.pop(0)
        wf = workflows[next_wf]
        for step in wf:
            if not all(len(r) > 0 for r in ranges):
                # No possible combinations
                break
            if ":" not in step:
                next_wf = step
                targets[next_wf].append(dict(ranges))

                if next_wf not in ["A", "R"]:
                    queue.append((next_wf, ranges))
                break
            cond, nw = step.split(":")
            if ">" in cond:
                var, val = cond.split(">")
                val = int(val)
                new_ranges = {
                    k: v & set(range(val + 1, 4001)) if k == var else set(v)
                    for k, v in ranges.items()
                }

                # Trim the remaining ranges
                ranges = {
                    k: v & set(range(1, val + 1)) if k == var else set(v)
                    for k, v in ranges.items()
                }

                # if nw not in targets:
                #    targets[nw] = {
                #        "x": set(),
                #        "m": set(),
                #        "a": set(),
                #        "s": set(),
                #    }
                # targets[nw] = {v: targets[nw][v] | new_ranges[v] for v in "xmas"}
                targets[nw].append(new_ranges)
                if nw not in ["A", "R"] and all(len(r) > 0 for r in new_ranges):
                    queue.append((nw, new_ranges))
            else:
                assert "<" in cond
                var, val = cond.split("<")
                val = int(val)
                new_ranges = {
                    k: v & set(range(1, val)) if k == var else set(v)
                    for k, v in ranges.items()
                }

                # Trim the remaining ranges
                ranges = {
                    k: v & set(range(val, 4001)) if k == var else set(v)
                    for k, v in ranges.items()
                }

                # if nw not in targets:
                #    targets[nw] = {
                #        "x": set(),
                #        "m": set(),
                #        "a": set(),
                #        "s": set(),
                #    }
                # targets[nw] = {v: targets[nw][v] | new_ranges[v] for v in "xmas"}
                targets[nw].append(new_ranges)
                if nw not in ["A", "R"] and all(len(r) > 0 for r in new_ranges):
                    queue.append((nw, new_ranges))
        # continue
    ranges = targets["A"]
    answer = 0
    for r in ranges:
        for v in "xmas":
            if len(r[v]) == 0:
                print(f"{v}: None", end=" ")
            else:
                print(f"{v}: {min(r[v])}-{max(r[v])}", end=" ")
        print()
        answer += prod([len(v) for v in r.values()])
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
