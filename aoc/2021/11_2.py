from io import TextIOWrapper
import io
import math
import numpy as np


def solve(inp: TextIOWrapper):
    answer = 0

    inp2 = io.StringIO(
        """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    )
    energy = np.array([[int(n) for n in list(l.strip())] for l in inp.readlines()])
    rows = len(energy)
    cols = len(energy[0])

    step = 0
    while True:
        step += 1
        # print(energy)

        flashed = set()
        energy = energy + 1

        flash_queue = [
            (r, c) for r in range(rows) for c in range(cols) if energy[r, c] > 9
        ]

        while len(flash_queue) > 0:
            flash_r, flash_c = flash_queue.pop(0)
            if (flash_r, flash_c) in flashed:
                continue
            flashed.add((flash_r, flash_c))
            for r, c in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                neigh = flash_r + r, flash_c + c
                if neigh[0] < 0 or neigh[0] >= rows or neigh[1] < 0 or neigh[1] >= cols:
                    continue
                energy[neigh] += 1
                if (
                    energy[flash_r + r, flash_c + c] > 9
                    and (flash_r + r, flash_c + c) not in flashed
                ):
                    flash_queue.append((flash_r + r, flash_c + c))

        energy[energy > 9] = 0
        # print(flashed)
        if len(flashed) == rows * cols:
            return step
