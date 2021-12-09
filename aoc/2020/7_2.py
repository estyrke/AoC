from typing import DefaultDict

# ## --- Part Two ---
#
# It's getting pretty expensive to fly these days - not because of
# ticket prices, but because of the ridiculous number of bags you need
# to buy!
#
# Consider again your `shiny gold` bag and the rules from the above
# example:
#
# * `faded blue` bags contain `0` other bags.
# * `dotted black` bags contain `0` other bags.
# * `vibrant plum` bags contain `11` other bags: 5 `faded blue` bags and
# 6 `dotted black` bags.
# * `dark olive` bags contain `7` other bags: 3 `faded blue` bags and 4
# `dotted black` bags.
#
#
# So, a single `shiny gold` bag must contain 1 `dark olive` bag (and the
# 7 bags within it) plus 2 `vibrant plum` bags (and the 11 bags within
# *each* of those): `1 + 1*7 + 2 + 2*11` = `*32*` bags!
#
# Of course, the actual rules have a small chance of going several
# levels deeper than this example; be sure to count all of the bags,
# even if the nesting becomes topologically impractical!
#
# Here's another example:
#
#
# ```
# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
#
# ```
#
# In this example, a single `shiny gold` bag must contain `*126*` other
# bags.
#
# *How many individual bags are required inside your single `shiny gold`
# bag?*


def solve(inp):
    test_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""
    parent_map = DefaultDict(lambda: list())
    child_map = DefaultDict(lambda: list())
    for line in inp.readlines():
        # for line in test_input.splitlines():
        parent, children = line.split(" contain ")
        parent = tuple(parent.split(" ", 2)[:2])
        if children.strip() == "no other bags.":
            parent_map[parent] = []
            continue
        for child in children.split(","):
            num, mod, col = child.strip().split(" ", 3)[:3]
            parent_map[parent].append((int(num), mod, col))
            child_map[(mod, col)].append(parent)

    def count_children(color):
        total_children = 0
        for num, mod, col in parent_map[color]:
            total_children += num * (1 + count_children((mod, col)))
        return total_children

    answer = count_children(("shiny", "gold"))
    print(answer)
    return answer