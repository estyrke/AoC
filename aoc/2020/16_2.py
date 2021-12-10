from io import TextIOWrapper
import io
import math
from typing import DefaultDict
from itertools import permutations

###
# ## --- Part Two ---
#
# Now that you've identified which tickets contain invalid values,
# *discard those tickets entirely*. Use the remaining valid tickets to
# determine which field is which.
#
# Using the valid ranges for each field, determine what order the fields
# appear on the tickets. The order is consistent between all tickets: if
# `seat` is the third field, it is the third field on every ticket,
# including *your ticket*.
#
# For example, suppose you have the following notes:
#
#
# ```
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
#
# ```
#
# Based on the *nearby tickets* in the above example, the first position
# must be `row`, the second position must be `class`, and the third
# position must be `seat`; you can conclude that in *your ticket*,
# `class` is `12`, `row` is `11`, and `seat` is `13`.
#
# Once you work out which field is which, look for the six fields on
# *your ticket* that start with the word `departure`. *What do you get
# if you multiply those six values together?*
###


def solve(inp: TextIOWrapper):
    test_input = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    fields = {}
    possible_fields = DefaultDict(set)
    # inp = io.StringIO(test_input)
    while True:
        line = inp.readline()
        if line.strip() == "":
            break
        field, values = line.strip().split(": ")
        range1, range2 = values.split(" or ")
        min1, max1 = [int(x) for x in range1.split("-")]
        min2, max2 = [int(x) for x in range2.split("-")]

        for i in range(min1, max1 + 1):
            possible_fields[i].add(field)
        for i in range(min2, max2 + 1):
            possible_fields[i].add(field)
        fields[field] = (min1, max1, min2, max2)

    assert inp.readline().strip() == "your ticket:"
    my_ticket = [int(n) for n in inp.readline().strip().split(",")]
    inp.readline()

    assert inp.readline().strip() == "nearby tickets:"

    nearby_tickets = [[int(n) for n in l.strip().split(",")] for l in inp.readlines()]

    field_idx = {}
    nearby_tickets = [
        t
        for t in nearby_tickets
        if all([n in possible_fields and len(possible_fields[n]) > 0 for n in t])
    ]

    remaining_indices = set(range(len(fields)))
    while len(fields) > 0:
        print(fields)

        for i in list(remaining_indices):
            all_values = [t[i] for t in nearby_tickets]
            candidates = []
            for field, (min1, max1, min2, max2) in fields.items():
                if not all(
                    [
                        v >= min1 and v <= max1 or v >= min2 and v <= max2
                        for v in all_values
                    ]
                ):
                    continue
                candidates.append(field)

            if len(candidates) == 1:
                field = candidates[0]
                field_idx[field] = i
                del fields[field]
                remaining_indices.discard(i)

    answer = 1
    departure_fields = [f for f in field_idx.keys() if f.startswith("departure")]
    print(departure_fields)
    for field in departure_fields:
        answer *= my_ticket[field_idx[field]]

    return answer
