from io import TextIOWrapper
import math
import functools
import itertools
from ..tools import parse_input

part1_test_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

part1_test_output = 64


def part1(inp: TextIOWrapper):
    answer = 0

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    pixels = [tokens for tokens in parse_input(inp, "{:d},{:d},{:d}")]
    pixel_set = set(pixels)
    for x, y, z in pixel_set:
        exposed = 6
        if (x, y, z + 1) in pixel_set:
            exposed -= 1
        if (x, y, z - 1) in pixel_set:
            exposed -= 1
        if (x, y + 1, z) in pixel_set:
            exposed -= 1
        if (x, y - 1, z) in pixel_set:
            exposed -= 1
        if (x + 1, y, z) in pixel_set:
            exposed -= 1
        if (x - 1, y, z) in pixel_set:
            exposed -= 1
        answer += exposed
    return answer


part2_test_input = part1_test_input

part2_test_output = 58

import numpy as np
import skimage.segmentation as ss


def part2(inp: TextIOWrapper):
    answer = 0

    pixels = [tokens for tokens in parse_input(inp, "{:d},{:d},{:d}")]
    pixel_set = set(pixels)
    min_x, max_x = (
        min(pixels, key=lambda p: p[0])[0],
        max(pixels, key=lambda p: p[0])[0],
    )
    min_y, max_y = (
        min(pixels, key=lambda p: p[1])[1],
        max(pixels, key=lambda p: p[1])[1],
    )
    min_z, max_z = (
        min(pixels, key=lambda p: p[2])[2],
        max(pixels, key=lambda p: p[2])[2],
    )

    image = np.zeros(shape=(max_z + 1, max_y + 1, max_x + 1), dtype=np.uint8)

    for x, y, z in pixel_set:
        image[z, y, x] = 1
    image = np.pad(image, pad_width=1, mode="constant", constant_values=0)
    image = ss.flood_fill(image, (0, 0, 0), 2, connectivity=1)
    for x, y, z in pixel_set:
        # Account for padding
        x += 1
        y += 1
        z += 1
        exposed = 6
        if image[(z, y, x + 1)] < 2:
            exposed -= 1
        if image[(z, y, x - 1)] < 2:
            exposed -= 1
        if image[(z, y + 1, x)] < 2:
            exposed -= 1
        if image[(z, y - 1, x)] < 2:
            exposed -= 1
        if image[(z + 1, y, x)] < 2:
            exposed -= 1
        if image[(z - 1, y, x)] < 2:
            exposed -= 1
        answer += exposed
    return answer
