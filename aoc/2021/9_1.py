from io import TextIOWrapper
import math

###
# # ## --- Day 9: Smoke Basin ---
#
# These caves seem to be [lava
# tubes](https://en.wikipedia.org/wiki/Lava_tube). Parts are even still
# volcanically active; small hydrothermal vents release smoke into the
# caves that slowly settles like rain.
#
# If you can model how the smoke flows through the caves, you might be
# able to avoid it and be that much safer. The submarine generates a
# heightmap of the floor of the nearby caves for you (your puzzle
# input).
#
# Smoke flows to the lowest point of the area it's in. For example,
# consider the following heightmap:
#
#
# ```
# 2*1*9994321*0*
# 3987894921
# 98*5*6789892
# 8767896789
# 989996*5*678
#
# ```
#
# Each number corresponds to the height of a particular location, where
# `9` is the highest and `0` is the lowest a location can be.
#
# Your first goal is to find the *low points* - the locations that are
# lower than any of its adjacent locations. Most locations have four
# adjacent locations (up, down, left, and right); locations on the edge
# or corner of the map have three or two adjacent locations,
# respectively. (Diagonal locations do not count as adjacent.)
#
# In the above example, there are *four* low points, all highlighted:
# two are in the first row (a `1` and a `0`), one is in the third row (a
# `5`), and one is in the bottom row (also a `5`). All other locations
# on the heightmap have some lower adjacent location, and so are not low
# points.
#
# The *risk level* of a low point is *1 plus its height*. In the above
# example, the risk levels of the low points are `2`, `1`, `6`, and `6`.
# The sum of the risk levels of all low points in the heightmap is
# therefore `*15*`.
#
# Find all of the low points on your heightmap. *What is the sum of the
# risk levels of all low points on your heightmap?*
###


def is_lowest(hmap, row, col):
    target = hmap[row][col]
    max_row = len(hmap) - 1
    max_col = len(hmap[0]) - 1

    for row_d in [-1, 0, 1]:
        for col_d in [-1, 0, 1]:
            if row_d == col_d:
                continue

            test_row = row
            test_col = col
            test_row, test_col = test_row + row_d, test_col + col_d
            if test_row < 0 or test_col < 0 or test_row > max_row or test_col > max_col:
                continue

            if target >= hmap[test_row][test_col]:
                return False
            # while True:
            #    test_row, test_col = test_row + row_d, test_col + col_d
            #    if (
            #        test_row < 0
            #        or test_col < 0
            #        or test_row > max_row
            #        or test_col > max_col
            #    ):
            #        break
            #    if seats[test_row][test_col] == "#":
            #        occ += 1
            #        break
            #    elif seats[test_row][test_col] == "L":
            #        break
    return True


def solve(inp: TextIOWrapper):
    hmap = []
    for line in inp.readlines():
        hmap.append([int(i) for i in list(line.strip())])

    answer = 0
    for y, row in enumerate(hmap):
        for x, col in enumerate(row):
            if is_lowest(hmap, y, x):
                answer += col + 1

    return answer
