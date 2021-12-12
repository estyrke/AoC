from typing import DefaultDict

# ## --- Part Two ---
#
# Unfortunately, considering only horizontal and vertical lines doesn't
# give you the full picture; you need to also consider *diagonal lines*.
#
# Because of the limits of the hydrothermal vent mapping system, the
# lines in your list will only ever be horizontal, vertical, or a
# diagonal line at exactly 45 degrees. In other words:
#
# * An entry like `1,1 -> 3,3` covers points `1,1`, `2,2`, and `3,3`.
# * An entry like `9,7 -> 7,9` covers points `9,7`, `8,8`, and `7,9`.
#
#
# Considering all lines from the above example would now produce the
# following diagram:
#
#
# ```
# 1.1....11.
# .111...2..
# ..2.1.111.
# ...1.2.2..
# .112313211
# ...1.2....
# ..1...1...
# .1.....1..
# 1.......1.
# 222111....
#
# ```
#
# You still need to determine *the number of points where at least two
# lines overlap*. In the above example, this is still anywhere in the
# diagram with a `2` or larger - now a total of `*12*` points.
#
# Consider all of the lines. *At how many points do at least two lines
# overlap?*


def solve(inp):
    board = DefaultDict(lambda: 0)
    test_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    for line in inp.readlines():
        # for line in test_input.splitlines():
        p1, p2 = line.split(" -> ")
        x1, y1 = (int(i) for i in p1.split(","))
        x2, y2 = (int(i) for i in p2.split(","))
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                board[(x1, y)] += 1
        elif y1 == y2:
            for i, x in enumerate(range(min(x1, x2), max(x1, x2) + 1)):
                board[(x, y1)] += 1
        else:
            if x1 < x2:
                ys = y1
                ye = y2
            else:
                ys = y2
                ye = y1
            delta = 1 if ye > ys else -1
            for i, x in enumerate(range(min(x1, x2), max(x1, x2) + 1)):
                board[(x, ys + delta * i)] += 1

    answer = 0
    for v in board.values():
        if v > 1:
            answer += 1
    return answer
