from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# You still can't quite make out the details in the image. Maybe you
# just didn't
# [enhance](https://en.wikipedia.org/wiki/Kernel_(image_processing)) it
# enough.
#
# If you enhance the starting input image in the above example a total
# of *50* times, `*3351*` pixels are lit in the final output image.
#
# Start again with the original input image and apply the image
# enhancement algorithm 50 times. *How many pixels are lit in the
# resulting image?*
###

test_input = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


test_output = 3351

import numpy as np
import scipy.signal as sig

KERNEL = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]])[::-1, ::-1]


def solve(inp: TextIOWrapper):
    answer = None

    algo = np.array([1 if p == "#" else 0 for p in inp.readline().strip()])
    assert inp.readline().strip() == ""
    image = np.array(
        [[1 if p == "#" else 0 for p in list(l.strip())] for l in inp.readlines()]
    )

    image = np.pad(image, 1, constant_values=0)
    for i in range(50):
        image = enhance(image, algo)
    answer = len(image[image == 1])
    return answer


def enhance(image, algo):
    image = np.pad(image, 1, "edge")
    out_image = sig.convolve2d(image, KERNEL, mode="valid")
    out_image = algo[out_image]

    out_image = np.pad(
        out_image, 1, constant_values=algo[np.sum(np.multiply(image[0, 0], KERNEL))]
    )

    return out_image
