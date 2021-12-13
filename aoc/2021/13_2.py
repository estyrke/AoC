from io import StringIO, TextIOWrapper
import math
from typing import Set, Tuple

###
# ## --- Part Two ---
#
# Finish folding the transparent paper according to the instructions.
# The manual says the code is always *eight capital letters*.
#
# *What code do you use to activate the infrared thermal imaging camera
# system?*
###

def fold_y(coords: Set[Tuple[int, int]], line, rows, new_rows):
    new_coords = set()
    for x, y in coords:
        if y > line:
            new_coords.add((x, rows-y if rows % 2 == 0 else rows-y-1))
        else:
            new_coords.add((x, y))
    return new_coords

def fold_x(coords: Set[Tuple[int, int]], col, cols, new_cols):
    new_coords = set()
    for x, y in coords:
        if x > col:
            new_coords.add((cols-x if cols % 2 == 0 else cols-x-1, y))
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

    rows = max([y for x, y in coords])+1
    cols = max([x for x, y in coords])+1
    for dir, idx in folds:

        print(rows, cols, dir, idx)

        if dir == "y":
            fold_row = int(idx)
            new_rows = max(fold_row, rows-fold_row-1)
            #assert new_rows == rows / 2
            print(rows, new_rows)
            coords = fold_y(coords, int(idx), rows, new_rows)
            rows = new_rows
        else:
            fold_col = int(idx)
            new_cols = max(fold_col, cols-fold_col-1)
            #assert new_cols == cols / 2

            print(cols, new_cols)
            coords = fold_x(coords, fold_col, cols, new_cols)
            cols = new_cols

    #rint(coords)
    for y in range(rows):
        for x in range(cols):
            if (x,y) in coords:
                print("#",end="")
            else:
                print(".", end="")
        print()
    return len(coords)
