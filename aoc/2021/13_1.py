from io import StringIO, TextIOWrapper
import math
from typing import Set, Tuple

###
# # ## --- Day 13: Transparent Origami ---
#
# You reach another volcanically active part of the cave. It would be
# nice if you could do some kind of thermal imaging so you could tell
# ahead of time which caves are too hot to safely enter.
#
# Fortunately, the submarine seems to be equipped with a thermal camera!
# When you activate it, you are greeted with:
#
#
# ```
# Congratulations on your purchase! To activate this infrared thermal imaging
# camera system, please enter the code found on page 1 of the manual.
#
# ```
#
# Apparently, the Elves have never used this feature. To your surprise,
# you manage to find the manual; as you go to open it, page 1 falls out.
# It's a large sheet of [transparent
# paper](https://en.wikipedia.org/wiki/Transparency_(projection))! The
# transparent paper is marked with random dots and includes instructions
# on how to fold it up (your puzzle input). For example:
#
#
# ```
# 6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0
#
# fold along y=7
# fold along x=5
#
# ```
#
# The first section is a list of dots on the transparent paper. `0,0`
# represents the top-left coordinate. The first value, `x`, increases to
# the right. The second value, `y`, increases downward. So, the
# coordinate `3,0` is to the right of `0,0`, and the coordinate `0,7` is
# below `0,0`. The coordinates in this example form the following
# pattern, where `#` is a dot on the paper and `.` is an empty, unmarked
# position:
#
#
# ```
# ...#..#..#.
# ....#......
# ...........
# #..........
# ...#....#.#
# ...........
# ...........
# ...........
# ...........
# ...........
# .#....#.##.
# ....#......
# ......#...#
# #..........
# #.#........
#
# ```
#
# Then, there is a list of *fold instructions*. Each instruction
# indicates a line on the transparent paper and wants you to fold the
# paper *up* (for horizontal `y=...` lines) or *left* (for vertical
# `x=...` lines). In this example, the first fold instruction is `fold
# along y=7`, which designates the line formed by all of the positions
# where `y` is `7` (marked here with `-`):
#
#
# ```
# ...#..#..#.
# ....#......
# ...........
# #..........
# ...#....#.#
# ...........
# ...........
# -----------
# ...........
# ...........
# .#....#.##.
# ....#......
# ......#...#
# #..........
# #.#........
#
# ```
#
# Because this is a horizontal line, fold the bottom half *up*. Some of
# the dots might end up overlapping after the fold is complete, but dots
# will never appear exactly on a fold line. The result of doing this
# fold looks like this:
#
#
# ```
# #.##..#..#.
# #...#......
# ......#...#
# #...#......
# .#.#..#.###
# ...........
# ...........
#
# ```
#
# Now, only `17` dots are visible.
#
# Notice, for example, the two dots in the bottom left corner before the
# transparent paper is folded; after the fold is complete, those dots
# appear in the top left corner (at `0,0` and `0,1`). Because the paper
# is transparent, the dot just below them in the result (at `0,3`)
# remains visible, as it can be seen through the transparent paper.
#
# Also notice that some dots can end up *overlapping*; in this case, the
# dots merge together and become a single dot.
#
# The second fold instruction is `fold along x=5`, which indicates this
# line:
#
#
# ```
# #.##.|#..#.
# #...#|.....
# .....|#...#
# #...#|.....
# .#.#.|#.###
# .....|.....
# .....|.....
#
# ```
#
# Because this is a vertical line, fold *left*:
#
#
# ```
# #####
# #...#
# #...#
# #...#
# #####
# .....
# .....
#
# ```
#
# The instructions made a square!
#
# The transparent paper is pretty big, so for now, focus on just
# completing the first fold. After the first fold in the example above,
# `*17*` dots are visible - dots that end up overlapping after the fold
# is completed count as a single dot.
#
# *How many dots are visible after completing just the first fold
# instruction on your transparent paper?*
###

def fold_y(coords: Set[Tuple[int, int]], line, rows, new_rows):
    new_coords = set()
    for x, y in coords:
        if y > line:
            new_coords.add((x, rows-y))
        else:
            new_coords.add((x, y))
    return new_coords

def fold_x(coords: Set[Tuple[int, int]], col, cols, new_cols):
    new_coords = set()
    for x, y in coords:
        if x > col:
            new_coords.add((cols-x, y))
        else:
            new_coords.add((x, y))
    return new_coords

def solve(inp: TextIOWrapper):
    test_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    inp2 = StringIO(test_input)
    # for line in inp.readlines():
    lines = [l for l in inp.readlines()]

    coords = [tuple(line.strip().split(",")) for line in lines if len(line.strip()) > 0 and not line.startswith("fold along")]
    folds =  [line.strip().split()[-1].split("=") for line in lines if line.startswith("fold along")]

    coords = set([(int(x), int(y)) for x, y in coords])

    print(coords)

    rows = max([y for x, y in coords])+1
    cols = max([x for x, y in coords])+1
    for dir, idx in folds:
        print(dir, idx)
        if dir == "y":
            fold_row = int(idx)
            new_rows = max(fold_row, rows-fold_row-1)
            print(rows, new_rows)
            coords = fold_y(coords, int(idx), rows, new_rows)
            rows = new_rows
        else:
            fold_col = int(idx)
            new_cols = max(fold_col, cols-fold_col-1)
            print(cols, new_cols)
            coords = fold_x(coords, fold_col, cols, new_cols)
            cols = new_cols
        break

    print(coords)
    return len(coords)
