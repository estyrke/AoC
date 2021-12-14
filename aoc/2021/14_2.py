from collections import defaultdict
from io import TextIOWrapper
import math
from typing import DefaultDict

###
# ## --- Part Two ---
#
# The resulting polymer isn't nearly strong enough to reinforce the
# submarine. You'll need to run more steps of the pair insertion
# process; a total of *40 steps* should do it.
#
# In the above example, the most common element is `B` (occurring
# `2192039569602` times) and the least common element is `H` (occurring
# `3849876073` times); subtracting these produces `*2188189693529*`.
#
# Apply *40* steps of pair insertion to the polymer template and find
# the most and least common elements in the result. *What do you get if
# you take the quantity of the most common element and subtract the
# quantity of the least common element?*
###

test_input = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

test_output = 2188189693529

def do_insert(pairs, rules):
    new_pairs = defaultdict(int)
    for pair, count in pairs.items():
        if pair in rules:
            pair1 = pair[0] + rules[pair]
            pair2 = rules[pair] + pair[1]
            new_pairs[pair1] += count
            new_pairs[pair2] += count
        else:
            new_pairs[pair] += count
    return new_pairs

def solve(inp: TextIOWrapper):
    answer = None

    templ, rules = inp.read().split("\n\n")

    templ = templ.strip()
    rules = [r.strip().split(" -> ") for r in rules.splitlines()]
    rules = {r[0]: r[1] for r in rules}

    pairs = DefaultDict(int)
    for i in range(len(templ)-1):
        pair = templ[i] + templ[i+1]
        pairs[pair] += 1

    print(pairs)
    print(rules)
    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    res = pairs
    for i in range(40):
        res = do_insert(res, rules)

    counts = defaultdict(int)
    print(res)
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for pair, count in res.items():
            if pair.startswith(c):
                counts[c] += count

    counts[templ[-1]] += 1
    counts = sorted(counts.items(), key=lambda c: c[1])
    print(counts)
    return counts[-1][1] - counts[0][1]
