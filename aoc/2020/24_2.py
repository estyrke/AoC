from io import TextIOWrapper
import math
from typing import Tuple

###
# ## --- Part Two ---
#
# The tile floor in the lobby is meant to be a living art exhibit. Every
# day, the tiles are all flipped according to the following rules:
#
# * Any *black* tile with *zero* or *more than 2* black tiles
# immediately adjacent to it is flipped to *white*.
# * Any *white* tile with *exactly 2* black tiles immediately adjacent
# to it is flipped to *black*.
#
#
# Here, *tiles immediately adjacent* means the six tiles directly
# touching the tile in question.
#
# The rules are applied *simultaneously* to every tile; put another way,
# it is first determined which tiles need to be flipped, then they are
# all flipped at the same time.
#
# In the above example, the number of black tiles that are facing up
# after the given number of days has passed is as follows:
#
#
# ```
# Day 1: 15
# Day 2: 12
# Day 3: 25
# Day 4: 14
# Day 5: 23
# Day 6: 28
# Day 7: 41
# Day 8: 37
# Day 9: 49
# Day 10: 37
#
# Day 20: 132
# Day 30: 259
# Day 40: 406
# Day 50: 566
# Day 60: 788
# Day 70: 1106
# Day 80: 1373
# Day 90: 1844
# Day 100: 2208
#
# ```
#
# After executing this process a total of 100 times, there would be
# *`2208`* black tiles facing up.
#
# *How many tiles will be black after 100 days?*
###

test_input = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

test_output = 2208


def walk(directions: str) -> Tuple[float, float]:
    x, y = 0, 0
    while len(directions):
        if directions.startswith("se"):
            x, y = x + 0.5, y + 1
            directions = directions[2:]
        elif directions.startswith("sw"):
            x, y = x - 0.5, y + 1
            directions = directions[2:]
        elif directions.startswith("ne"):
            x, y = x + 0.5, y - 1
            directions = directions[2:]
        elif directions.startswith("nw"):
            x, y = x - 0.5, y - 1
            directions = directions[2:]
        elif directions.startswith("e"):
            x += 1
            directions = directions[1:]
        else:
            assert directions.startswith("w")
            x -= 1
            directions = directions[1:]
    return (x, y)


def num_black_adj(tiles, x, y) -> int:
    return [
        tiles.get(coord, False)
        for coord in [
            (x + 1, y),
            (x - 1, y),
            (x + 0.5, y + 1),
            (x - 0.5, y + 1),
            (x + 0.5, y - 1),
            (x - 0.5, y - 1),
        ]
    ].count(True)


def solve(inp: TextIOWrapper):
    black_tiles = {}
    for line in inp.readlines():
        coord = walk(line.strip())
        black_tiles[coord] = not black_tiles.get(coord, False)

    face_up = len([v for v in black_tiles.values() if v])

    for _ in range(100):
        min_x = min([math.floor(x) for x, y in black_tiles.keys()])
        max_x = max([math.ceil(x) for x, y in black_tiles.keys()])
        min_y = min([y for x, y in black_tiles.keys()])
        max_y = max([y for x, y in black_tiles.keys()])

        new_layout = {k: v for k, v in black_tiles.items()}
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                if y % 2 != 0:
                    x += 0.5
                is_black = black_tiles.get((x, y), False)
                adj = num_black_adj(black_tiles, x, y)
                if is_black and (adj == 0 or adj > 2):
                    del new_layout[(x, y)]
                elif not is_black and adj == 2:
                    new_layout[(x, y)] = True

        black_tiles = new_layout
        face_up = len([v for v in black_tiles.values() if v])
    return face_up
