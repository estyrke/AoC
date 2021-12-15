from collections import defaultdict
from io import TextIOWrapper
import math
from typing import Any, DefaultDict, Dict, Generator, List, Tuple

###
# # ## --- Day 20: Jurassic Jigsaw ---
#
# The high-speed train leaves the forest and quickly carries you south.
# You can even see a desert in the distance! Since you have some spare
# time, you might as well see if there was anything interesting in the
# image the Mythical Information Bureau satellite captured.
#
# After decoding the satellite messages, you discover that the data
# actually contains many small images created by the satellite's *camera
# array*. The camera array consists of many cameras; rather than produce
# a single square image, they produce many smaller square image *tiles*
# that need to be *reassembled back into a single image*.
#
# Each camera in the camera array returns a single monochrome *image
# tile* with a random unique *ID number*. The tiles (your puzzle input)
# arrived in a random order.
#
# Worse yet, the camera array appears to be malfunctioning: each image
# tile has been *rotated and flipped to a random orientation*. Your
# first task is to reassemble the original image by orienting the tiles
# so they fit together.
#
# To show how the tiles should be reassembled, each tile's image data
# includes a border that should line up exactly with its adjacent tiles.
# All tiles have this border, and the border lines up exactly when the
# tiles are both oriented correctly. Tiles at the edge of the image also
# have this border, but the outermost edges won't line up with any other
# tiles.
#
# For example, suppose you have the following nine tiles:
#
#
# ```
# Tile 2311:
# ..##.#..#.
# ##..#.....
# #...##..#.
# ####.#...#
# ##.##.###.
# ##...#.###
# .#.#.#..##
# ..#....#..
# ###...#.#.
# ..###..###
#
# Tile 1951:
# #.##...##.
# #.####...#
# .....#..##
# #...######
# .##.#....#
# .###.#####
# ###.##.##.
# .###....#.
# ..#.#..#.#
# #...##.#..
#
# Tile 1171:
# ####...##.
# #..##.#..#
# ##.#..#.#.
# .###.####.
# ..###.####
# .##....##.
# .#...####.
# #.##.####.
# ####..#...
# .....##...
#
# Tile 1427:
# ###.##.#..
# .#..#.##..
# .#.##.#..#
# #.#.#.##.#
# ....#...##
# ...##..##.
# ...#.#####
# .#.####.#.
# ..#..###.#
# ..##.#..#.
#
# Tile 1489:
# ##.#.#....
# ..##...#..
# .##..##...
# ..#...#...
# #####...#.
# #..#.#.#.#
# ...#.#.#..
# ##.#...##.
# ..##.##.##
# ###.##.#..
#
# Tile 2473:
# #....####.
# #..#.##...
# #.##..#...
# ######.#.#
# .#...#.#.#
# .#########
# .###.#..#.
# ########.#
# ##...##.#.
# ..###.#.#.
#
# Tile 2971:
# ..#.#....#
# #...###...
# #.#.###...
# ##.##..#..
# .#####..##
# .#..####.#
# #..#.#..#.
# ..####.###
# ..#.#.###.
# ...#.#.#.#
#
# Tile 2729:
# ...#.#.#.#
# ####.#....
# ..#.#.....
# ....#..#.#
# .##..##.#.
# .#.####...
# ####.#.#..
# ##.####...
# ##..#.##..
# #.##...##.
#
# Tile 3079:
# #.#.#####.
# .#..######
# ..#.......
# ######....
# ####.#..#.
# .#...#.##.
# #.#####.##
# ..#.###...
# ..#.......
# ..#.###...
#
# ```
#
# By rotating, flipping, and rearranging them, you can find a square
# arrangement that causes all adjacent borders to line up:
#
#
# ```
# #...##.#.. ..###..### #.#.#####.
# ..#.#..#.# ###...#.#. .#..######
# .###....#. ..#....#.. ..#.......
# ###.##.##. .#.#.#..## ######....
# .###.##### ##...#.### ####.#..#.
# .##.#....# ##.##.###. .#...#.##.
# #...###### ####.#...# #.#####.##
# .....#..## #...##..#. ..#.###...
# #.####...# ##..#..... ..#.......
# #.##...##. ..##.#..#. ..#.###...
#
# #.##...##. ..##.#..#. ..#.###...
# ##..#.##.. ..#..###.# ##.##....#
# ##.####... .#.####.#. ..#.###..#
# ####.#.#.. ...#.##### ###.#..###
# .#.####... ...##..##. .######.##
# .##..##.#. ....#...## #.#.#.#...
# ....#..#.# #.#.#.##.# #.###.###.
# ..#.#..... .#.##.#..# #.###.##..
# ####.#.... .#..#.##.. .######...
# ...#.#.#.# ###.##.#.. .##...####
#
# ...#.#.#.# ###.##.#.. .##...####
# ..#.#.###. ..##.##.## #..#.##..#
# ..####.### ##.#...##. .#.#..#.##
# #..#.#..#. ...#.#.#.. .####.###.
# .#..####.# #..#.#.#.# ####.###..
# .#####..## #####...#. .##....##.
# ##.##..#.. ..#...#... .####...#.
# #.#.###... .##..##... .####.##.#
# #...###... ..##...#.. ...#..####
# ..#.#....# ##.#.#.... ...##.....
#
# ```
#
# For reference, the IDs of the above tiles are:
#
#
# ```
# *1951*    2311    *3079*
# 2729    1427    2473
# *2971*    1489    *1171*
#
# ```
#
# To check that you've assembled the image correctly, multiply the IDs
# of the four corner tiles together. If you do this with the assembled
# tiles from the example above, you get `1951 * 3079 * 2971 * 1171` =
# *`20899048083289`*.
#
# Assemble the tiles into an image. *What do you get if you multiply
# together the IDs of the four corner tiles?*
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

test_output = 20899048083289


import numpy as np


def solve(inp: TextIOWrapper):
    answer = None

    tiles: Dict[Tuple[int, bool], List[str]] = {}
    tile_id = 0
    tile: np.ndarray = np.empty(())
    for line in inp.readlines():
        if line.startswith("Tile"):
            tile_id = int(line.strip()[:-1].split()[1])
            tile = np.empty(())
        elif line.strip() == "":
            tiles[(tile_id, False)] = list(generate_tile_edges(tile))
            tiles[(tile_id, True)] = list(generate_reverse_tile_edges(tile))
        else:
            row = list(line.strip())
            if tile.shape == ():
                tile = np.array([row])
            else:
                tile = np.concatenate((tile, [row]), axis=0)
    tiles[(tile_id, False)] = list(generate_tile_edges(tile))
    tiles[(tile_id, True)] = list(generate_reverse_tile_edges(tile))

    tile_edges = DefaultDict(set)
    for (tile_id, rev), edges in tiles.items():
        for edge in edges:
            tile_edges[edge].add((tile_id, rev))

    rows = cols = int(math.sqrt(len(tiles) / 2))
    assert rows * cols * 2 == len(tiles)
    image = assemble(tiles, tile_edges, rows, cols, 0, 0, [None] * rows, None)
    return (
        image[0] * image[cols - 1] * image[(rows - 1) * cols] * image[rows * cols - 1]
    )


def assemble(tiles, tile_edges, rows, cols, row, col, row_constraints, col_constraint):
    next_col = (col + 1) % cols
    next_row = row + 1 if next_col == 0 else row
    next_row_constraints = row_constraints[:]

    if row == rows:
        assert len(tiles) == 0
        return []

    for (tile_id, rev), edges in tiles.items():
        for rotation in range(4):
            if row_constraints[col] is None or edges[rotation] == row_constraints[col]:
                if (
                    col_constraint is None
                    or edges[(rotation - 1) % 4] == col_constraint
                ):

                    next_row_constraints[col] = edges[(rotation + 2) % 4][::-1]
                    next_col_constraint = (
                        edges[(rotation + 1) % 4][::-1] if next_col != 0 else None
                    )
                    rest = assemble(
                        {k: v for k, v in tiles.items() if k[0] != tile_id},
                        tile_edges,
                        rows,
                        cols,
                        next_row,
                        next_col,
                        next_row_constraints,
                        next_col_constraint,
                    )
                    if rest is not None:
                        return [tile_id] + rest

    return None


def generate_tile_edges(tile: np.ndarray) -> Generator[str, None, None]:
    yield "".join(tile[0, :])
    yield "".join(tile[:, -1])
    yield "".join(tile[-1, ::-1])
    yield "".join(tile[::-1, 0])


def generate_reverse_tile_edges(tile: np.ndarray) -> Generator[str, None, None]:
    yield "".join(tile[:, 0])
    yield "".join(tile[-1, :])
    yield "".join(tile[::-1, -1])
    yield "".join(tile[0, ::-1])
