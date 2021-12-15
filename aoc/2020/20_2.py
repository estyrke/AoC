from collections import defaultdict
from io import TextIOWrapper
import math
from time import process_time_ns
from typing import Any, DefaultDict, Dict, Generator, List, Tuple

###
# ## --- Part Two ---
#
# Now, you're ready to *check the image for sea monsters*.
#
# The borders of each tile are not part of the actual image; start by
# removing them.
#
# In the example above, the tiles become:
#
#
# ```
# .#.#..#. ##...#.# #..#####
# ###....# .#....#. .#......
# ##.##.## #.#.#..# #####...
# ###.#### #...#.## ###.#..#
# ##.#.... #.##.### #...#.##
# ...##### ###.#... .#####.#
# ....#..# ...##..# .#.###..
# .####... #..#.... .#......
#
# #..#.##. .#..###. #.##....
# #.####.. #.####.# .#.###..
# ###.#.#. ..#.#### ##.#..##
# #.####.. ..##..## ######.#
# ##..##.# ...#...# .#.#.#..
# ...#..#. .#.#.##. .###.###
# .#.#.... #.##.#.. .###.##.
# ###.#... #..#.##. ######..
#
# .#.#.### .##.##.# ..#.##..
# .####.## #.#...## #.#..#.#
# ..#.#..# ..#.#.#. ####.###
# #..####. ..#.#.#. ###.###.
# #####..# ####...# ##....##
# #.##..#. .#...#.. ####...#
# .#.###.. ##..##.. ####.##.
# ...###.. .##...#. ..#..###
#
# ```
#
# Remove the gaps to form the actual image:
#
#
# ```
# .#.#..#.##...#.##..#####
# ###....#.#....#..#......
# ##.##.###.#.#..######...
# ###.#####...#.#####.#..#
# ##.#....#.##.####...#.##
# ...########.#....#####.#
# ....#..#...##..#.#.###..
# .####...#..#.....#......
# #..#.##..#..###.#.##....
# #.####..#.####.#.#.###..
# ###.#.#...#.######.#..##
# #.####....##..########.#
# ##..##.#...#...#.#.#.#..
# ...#..#..#.#.##..###.###
# .#.#....#.##.#...###.##.
# ###.#...#..#.##.######..
# .#.#.###.##.##.#..#.##..
# .####.###.#...###.#..#.#
# ..#.#..#..#.#.#.####.###
# #..####...#.#.#.###.###.
# #####..#####...###....##
# #.##..#..#...#..####...#
# .#.###..##..##..####.##.
# ...###...##...#...#..###
#
# ```
#
# Now, you're ready to search for sea monsters! Because your image is
# monochrome, a sea monster will look like this:
#
#
# ```
#                   #
# #    ##    ##    ###
#  #  #  #  #  #  #
#
# ```
#
# When looking for this pattern in the image, *the spaces can be
# anything*; only the `#` need to match. Also, you might need to rotate
# or flip your image before it's oriented correctly to find sea
# monsters. In the above image, *after flipping and rotating it* to the
# appropriate orientation, there are *two* sea monsters (marked with
# `*O*`):
#
#
# ```
# .####...#####..#...###..
# #####..#..#.#.####..#.#.
# .#.#...#.###...#.##.*O*#..
# #.*O*.##.*O**O*#.#.*O**O*.##.*O**O**O*##
# ..#*O*.#*O*#.*O*##*O*..*O*.#*O*##.##
# ...#.#..##.##...#..#..##
# #.##.#..#.#..#..##.#.#..
# .###.##.....#...###.#...
# #.####.#.#....##.#..#.#.
# ##...#..#....#..#...####
# ..#.##...###..#.#####..#
# ....#.##.#.#####....#...
# ..##.##.###.....#.##..#.
# #...#...###..####....##.
# .#.##...#.##.#.#.###...#
# #.###.#..####...##..#...
# #.###...#.##...#.##*O*###.
# .*O*##.#*O**O*.###*O**O*##..*O**O**O*##.
# ..*O*#.*O*..*O*..*O*.#*O*##*O*##.###
# #.#..##.########..#..##.
# #.#####..#.#...##..#....
# #....##..#.#########..##
# #...#.....#..##...###.##
# #..###....##.#...##.##.#
#
# ```
#
# Determine how rough the waters are in the sea monsters' habitat by
# counting the number of `#` that are *not* part of a sea monster. In
# the above example, the habitat's water roughness is *`273`*.
#
# *How many `#` are not part of a sea monster?*
###

test_input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

test_output = 273


import numpy as np


monster = """..................#.
#....##....##....###
.#..#..#..#..#..#..."""


def solve(inp: TextIOWrapper):
    tile_id = 0
    tile: np.ndarray = np.empty(())
    tile_data = {}
    for line in inp.readlines():
        if line.startswith("Tile"):
            tile_id = int(line.strip()[:-1].split()[1])
            tile = np.empty(())
        elif line.strip() == "":
            tile_data[tile_id] = tile
        else:
            row = [1 if c == "#" else 0 for c in line.strip()]
            if tile.shape == ():
                tile = np.array([row])
            else:
                tile = np.concatenate((tile, [row]), axis=0)
    tile_data[tile_id] = tile

    rows = cols = int(math.sqrt(len(tile_data)))
    assert rows * cols == len(tile_data)
    image_order = assemble(tile_data, rows, cols, 0, 0, [None] * rows, None)

    tile_size = list(tile_data.values())[0].shape[0]
    image = np.zeros((rows * (tile_size - 2), cols * (tile_size - 2)))
    for i, (tile_id, aligned) in enumerate(image_order):
        col = (i % cols) * (tile_size - 2)
        row = i // cols * (tile_size - 2)

        image[row : row + tile_size - 2, col : col + tile_size - 2] = aligned[
            1:-1, 1:-1
        ]

    monster_image = np.array(
        [[1 if c == "#" else 0 for c in l.strip("\n")] for l in monster.splitlines()]
    )
    monster_rows, monster_cols = monster_image.shape
    assert monster_rows, monster_cols == (3, 20)
    print("Finding monsters...")
    print(monster_image)
    for rev in [False, True]:
        for rotation in range(4):
            aligned = np.rot90(image, rotation)
            if rev:
                aligned = aligned.T

            monsters = 0
            for row in range(image.shape[0] - monster_rows + 1):
                for col in range(image.shape[1] - monster_cols + 1):
                    if np.all(
                        aligned[row : row + monster_rows, col : col + monster_cols]
                        >= monster_image
                    ):
                        aligned[
                            row : row + monster_rows, col : col + monster_cols
                        ] += monster_image
                        monsters += 1
            if monsters > 0:
                return len(aligned[aligned == 1])


def assemble(tiles, rows, cols, row, col, row_constraints, col_constraint):
    next_col = (col + 1) % cols
    next_row = row + 1 if next_col == 0 else row
    next_row_constraints = row_constraints[:]

    if row == rows:
        assert len(tiles) == 0
        return []

    for tile_id, tile_data in tiles.items():
        for rev in [True, False]:
            for rotation in range(4):
                aligned = np.rot90(tile_data, rotation)
                if rev:
                    aligned = aligned.T

                if row_constraints[col] is None or np.all(
                    aligned[0, :] == row_constraints[col]
                ):
                    if col_constraint is None or np.all(
                        aligned[:, 0] == col_constraint
                    ):
                        next_row_constraints[col] = aligned[-1, :]
                        next_col_constraint = aligned[:, -1] if next_col != 0 else None

                        rest = assemble(
                            {k: v for k, v in tiles.items() if k != tile_id},
                            rows,
                            cols,
                            next_row,
                            next_col,
                            next_row_constraints,
                            next_col_constraint,
                        )
                        if rest is not None:
                            return [(tile_id, aligned)] + rest

    return None
