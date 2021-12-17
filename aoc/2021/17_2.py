from io import TextIOWrapper
import math
from typing import Literal, Union


###
# ## --- Part Two ---
#
# Maybe a fancy trick shot isn't the best idea; after all, you only have
# one probe, so you had better not miss.
#
# To get the best idea of what your options are for launching the probe,
# you need to find *every initial velocity* that causes the probe to
# eventually be within the target area after any step.
#
# In the above example, there are `*112*` different initial velocity
# values that meet these criteria:
#
#
# ```
# 23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
# 25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
# 8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
# 26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
# 20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
# 25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
# 25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
# 8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
# 24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
# 7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
# 23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
# 27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
# 8,-2    27,-8   30,-5   24,-7
#
# ```
#
# *How many distinct initial velocity values cause the probe to be
# within the target area after any step?*
###

test_input = """target area: x=20..30, y=-10..-5
"""

test_output = 112


def solve(inp: TextIOWrapper):
    x, y = inp.read().strip().split(": ")[1].split(", ")
    minx, maxx = map(int, x[2:].split(".."))
    miny, maxy = map(int, y[2:].split(".."))

    xv_candidates = []
    for xv in range(1, maxx + 1):
        if hit_x(xv, minx, maxx + 1):
            xv_candidates.append(xv)

    yv_candidates = []
    for yv in range(miny - 1, 1000):
        if hit_y(yv, miny, maxy):
            yv_candidates.append(yv)

    ivs = []
    for yv in yv_candidates:
        for xv in xv_candidates:
            if hit(xv, yv, minx, maxx, miny, maxy):
                ivs.append((xv, yv))
    return len(ivs)


def hit_y(yv0: int, miny, maxy) -> bool:
    yv = yv0
    y = 0
    while True:
        y += yv
        if miny <= y <= maxy:
            return True
        if y < miny:
            return False
        yv -= 1


def hit_x(xv0: int, minx, maxx) -> bool:
    x = 0
    xv = xv0
    while True:
        x += xv
        if minx <= x <= maxx:
            return True
        if xv == 0:
            return False
        if xv > 0:
            xv -= 1


def hit(xv0: int, yv0: int, minx, maxx, miny, maxy) -> bool:
    y = 0
    x = 0
    xv = xv0
    yv = yv0
    while True:
        y += yv
        x += xv

        if minx <= x <= maxx and miny <= y <= maxy:
            return True
        if y < miny:
            return False
        if xv == 0 and (x < minx or x > maxx):
            return False
        if xv > 0:
            xv -= 1
        yv -= 1
