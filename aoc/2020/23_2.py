from io import TextIOWrapper
import math
from time import time_ns

###
# ## --- Part Two ---
#
# Due to what you can only assume is a mistranslation (you're not
# exactly fluent in Crab), you are quite surprised when the crab starts
# arranging *many* cups in a circle on your raft - *one million*
# (`1000000`) in total.
#
# Your labeling is still correct for the first few cups; after that, the
# remaining cups are just numbered in an increasing fashion starting
# from the number after the highest number in your list and proceeding
# one by one until one million is reached. (For example, if your
# labeling were `54321`, the cups would be numbered `5`, `4`, `3`, `2`,
# `1`, and then start counting up from `6` until one million is
# reached.) In this way, every number from one through one million is
# used exactly once.
#
# After discovering where you made the mistake in translating Crab
# Numbers, you realize the small crab isn't going to do merely 100
# moves; the crab is going to do *ten million* (`10000000`) moves!
#
# The crab is going to hide your *stars* - one each - under the *two
# cups that will end up immediately clockwise of cup `1`*. You can have
# them if you predict what the labels on those cups will be when the
# crab is finished.
#
# In the above example (`389125467`), this would be `934001` and then
# `159792`; multiplying these together produces *`149245887792`*.
#
# Determine which two cups will end up immediately clockwise of cup `1`.
# *What do you get if you multiply their labels together?*
###

test_input = """389125467"""

test_output = 149245887792


def pop_wrapped(cups, idx):
    if idx + 1 >= len(cups):
        idx = -1
    yield cups.pop(idx + 1)
    if idx + 1 >= len(cups):
        idx = -1
    yield cups.pop(idx + 1)
    if idx + 1 >= len(cups):
        idx = -1
    yield cups.pop(idx + 1)


def solve(inp: TextIOWrapper):
    inp_cups = [int(c) for c in inp.read().strip()]
    min_cup = min(inp_cups)
    max_cup = 1_000_000

    cups = inp_cups + list(range(max(inp_cups) + 1, max_cup + 1))
    next_cup = {c: cups[(i + 1) % len(cups)] for i, c in enumerate(cups)}

    current = inp_cups[0]

    for round in range(10_000_000):
        p1 = next_cup[current]
        p2 = next_cup[p1]
        p3 = next_cup[p2]
        new_next = next_cup[p3]
        next_cup[current] = new_next

        destination = current - 1
        while True:
            if destination < min_cup:
                destination = max_cup
            if destination in [p1, p2, p3]:
                destination -= 1
            else:
                break
        old_next = next_cup[destination]
        next_cup[destination] = p1
        next_cup[p3] = old_next

        current = next_cup[current]

    return next_cup[1] * next_cup[next_cup[1]]
