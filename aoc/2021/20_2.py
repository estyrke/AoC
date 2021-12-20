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


def solve(inp: TextIOWrapper):
    answer = None

    algo = [1 if p == "#" else 0 for p in inp.readline().strip()]
    assert inp.readline().strip() == ""
    image = np.array(
        [[1 if p == "#" else 0 for p in list(l.strip())] for l in inp.readlines()]
    )

    # index_img = np.convolve(image, kernel, )
    image = np.pad(image, 1, constant_values=0)
    for i in range(50):
        image = enhance(image, algo)
    answer = len(image[image == 1])
    return answer


def enhance(image, algo):
    kernel = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]])
    out_image = np.full_like(image, algo[0])
    image = np.pad(image, 1, "edge")
    for y in range(out_image.shape[0]):
        for x in range(out_image.shape[1]):
            pv = algo[np.sum(np.multiply(image[y : y + 3, x : x + 3], kernel))]
            out_image[y, x] = pv
    out_image = np.pad(
        out_image, 1, constant_values=algo[np.sum(np.multiply(image[0, 0], kernel))]
    )

    return out_image
