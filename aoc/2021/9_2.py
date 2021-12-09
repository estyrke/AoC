from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# Next, you need to find the largest basins so you know what areas are
# most important to avoid.
#
# A *basin* is all locations that eventually flow downward to a single
# low point. Therefore, every low point has a basin, although some
# basins are very small. Locations of height `9` do not count as being
# in any basin, and all other locations will always be part of exactly
# one basin.
#
# The *size* of a basin is the number of locations within the basin,
# including the low point. The example above has four basins.
#
# The top-left basin, size `3`:
#
#
# ```
# *21*99943210
# *3*987894921
# 9856789892
# 8767896789
# 9899965678
#
# ```
#
# The top-right basin, size `9`:
#
#
# ```
# 21999*43210*
# 398789*4*9*21*
# 985678989*2*
# 8767896789
# 9899965678
#
# ```
#
# The middle basin, size `14`:
#
#
# ```
# 2199943210
# 39*878*94921
# 9*85678*9892
# *87678*96789
# 9*8*99965678
#
# ```
#
# The bottom-right basin, size `9`:
#
#
# ```
# 2199943210
# 3987894921
# 9856789*8*92
# 876789*678*9
# 98999*65678*
#
# ```
#
# Find the three largest basins and multiply their sizes together. In
# the above example, this is `9 * 14 * 9 = *1134*`.
#
# *What do you get if you multiply together the sizes of the three
# largest basins?*
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


from scipy import ndimage as ndi
import numpy as np
from skimage.segmentation import watershed


def solve(inp: TextIOWrapper):
    hmap = []
    test_input = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    # for line in test_input.splitlines():
    for line in inp.readlines():
        hmap.append([int(i) for i in list(line.strip())])

    hmap = np.array(hmap)
    mask = hmap != 9
    wsi = watershed(hmap, mask=mask)
    num_basins = np.max(wsi)
    print(num_basins)
    sizes = [np.count_nonzero(wsi == i + 1) for i in range(num_basins)]

    sizes.sort(reverse=True)
    print(sizes)

    return math.prod(sizes[:3])
