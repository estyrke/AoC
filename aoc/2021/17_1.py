from io import TextIOWrapper
import math
from typing import Literal, Union

###
# # ## --- Day 17: Trick Shot ---
#
# You finally decode the Elves' message. `HI`, the message says. You
# continue searching for the sleigh keys.
#
# Ahead of you is what appears to be a large [ocean
# trench](https://en.wikipedia.org/wiki/Oceanic_trench). Could the keys
# have fallen into it? You'd better send a probe to investigate.
#
# The probe launcher on your submarine can fire the probe with any
# [integer](https://en.wikipedia.org/wiki/Integer) velocity in the `x`
# (forward) and `y` (upward, or downward if negative) directions. For
# example, an initial `x,y` velocity like `0,10` would fire the probe
# straight up, while an initial velocity like `10,-1` would fire the
# probe forward at a slight downward angle.
#
# The probe's `x,y` position starts at `0,0`. Then, it will follow some
# trajectory by moving in *steps*. On each step, these changes occur in
# the following order:
#
# * The probe's `x` position increases by its `x` velocity.
# * The probe's `y` position increases by its `y` velocity.
# * Due to drag, the probe's `x` velocity changes by `1` toward the
# value `0`; that is, it decreases by `1` if it is greater than `0`,
# increases by `1` if it is less than `0`, or does not change if it is
# already `0`.
# * Due to gravity, the probe's `y` velocity decreases by `1`.
#
#
# For the probe to successfully make it into the trench, the probe must
# be on some trajectory that causes it to be within a *target area*
# after any step. The submarine computer has already calculated this
# target area (your puzzle input). For example:
#
#
# ```
# target area: x=20..30, y=-10..-5
# ```
#
# This target area means that you need to find initial `x,y` velocity
# values such that after any step, the probe's `x` position is at least
# `20` and at most `30`, *and* the probe's `y` position is at least
# `-10` and at most `-5`.
#
# Given this target area, one initial velocity that causes the probe to
# be within the target area after any step is `7,2`:
#
#
# ```
# .............#....#............
# .......#..............#........
# ...............................
# S........................#.....
# ...............................
# ...............................
# ...........................#...
# ...............................
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTT#TT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
#
# ```
#
# In this diagram, `S` is the probe's initial position, `0,0`. The `x`
# coordinate increases to the right, and the `y` coordinate increases
# upward. In the bottom right, positions that are within the target area
# are shown as `T`. After each step (until the target area is reached),
# the position of the probe is marked with `#`. (The bottom-right `#` is
# both a position the probe reaches and a position in the target area.)
#
# Another initial velocity that causes the probe to be within the target
# area after any step is `6,3`:
#
#
# ```
# ...............#..#............
# ...........#........#..........
# ...............................
# ......#..............#.........
# ...............................
# ...............................
# S....................#.........
# ...............................
# ...............................
# ...............................
# .....................#.........
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................T#TTTTTTTTT
# ....................TTTTTTTTTTT
#
# ```
#
# Another one is `9,0`:
#
#
# ```
# S........#.....................
# .................#.............
# ...............................
# ........................#......
# ...............................
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTT#
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
#
# ```
#
# One initial velocity that *doesn't* cause the probe to be within the
# target area after any step is `17,-4`:
#
#
# ```
# S..............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# .................#.............................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT..#.............................
# ....................TTTTTTTTTTT................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ................................................#..............
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ..............................................................#
#
# ```
#
# The probe appears to pass through the target area, but is never within
# it after any step. Instead, it continues down and to the right - only
# the first few steps are shown.
#
# If you're going to fire a highly scientific probe out of a super cool
# probe launcher, you might as well do it with *style*. How high can you
# make the probe go while still reaching the target area?
#
# In the above example, using an initial velocity of `6,9` is the best
# you can do, causing the probe to reach a maximum `y` position of
# `*45*`. (Any higher initial `y` velocity causes the probe to overshoot
# the target area entirely.)
#
# Find the initial velocity that causes the probe to reach the highest
# `y` position and still eventually be within the target area after any
# step. *What is the highest `y` position it reaches on this
# trajectory?*
###

test_input = """target area: x=20..30, y=-10..-5
"""

test_output = None


def solve(inp: TextIOWrapper):
    x, y = inp.read().strip().split(": ")[1].split(", ")
    minx, maxx = map(int, x[2:].split(".."))
    miny, maxy = map(int, y[2:].split(".."))

    max_y = 0
    for i in range(-miny + 1):
        h = hit(i + 1, miny, maxy)
        if h is not False:
            max_y = max(max_y, h)

    return max_y


def hit(yv0: int, miny, maxy) -> Union[Literal[False], int]:
    t = 0
    y_prev = 0
    max_y = 0
    while True:
        t += 1
        y = y_prev + yv0 - t
        max_y = max(y, max_y)
        if y < miny:
            if miny <= y_prev <= maxy:
                return max_y
            return False
        y_prev = y
