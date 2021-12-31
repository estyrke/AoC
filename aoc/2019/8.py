from io import TextIOWrapper
import math

part1_test_input = """"""

part1_test_output = None

import numpy as np


def part1(inp: TextIOWrapper):
    pixels = list(map(int, inp.read().strip()))

    image = np.array(pixels)
    image.shape = (-1, 6, 25)

    nzero = np.count_nonzero(image, axis=(1, 2))
    ones = len(np.argwhere(image[np.argmax(nzero), :, :] == 1))
    twos = len(np.argwhere(image[np.argmax(nzero), :, :] == 2))

    return ones * twos


part2_test_input = None

part2_test_output = None


def part2(inp: TextIOWrapper):
    pixels = list(map(int, inp.read().strip()))

    image = np.array(pixels)
    image.shape = (-1, 6, 25)
    for y in range(image.shape[1]):
        for x in range(image.shape[2]):
            for z in range(image.shape[0]):
                if image[z, y, x] == 0:
                    print(" ", end=" ")
                    break
                elif image[z, y, x] == 1:
                    print("#", end=" ")
                    break
        print()

    return None
