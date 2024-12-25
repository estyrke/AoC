from io import StringIO, TextIOBase
import itertools
import sys

part1_test_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

part1_test_output = 3


def part1(inp: TextIOBase):
    answer = None

    locks_and_keys = inp.read().strip().split("\n\n")

    locks = []
    keys = []
    for lock_or_key_block in locks_and_keys:
        lock_or_key = lock_or_key_block.split("\n")
        heights = [0] * len(lock_or_key[0])
        for y, row in enumerate(lock_or_key):
            for x, cell in enumerate(row):
                if cell == "#":
                    heights[x] += 1
        if lock_or_key[0][0] == "#":
            locks.append(tuple(h - 1 for h in heights))
        else:
            keys.append(tuple(h - 1 for h in heights))

    answer = 0
    for lock, key in itertools.product(locks, keys):
        if all(k + l <= 5 for k, l in zip(key, lock)):
            answer += 1
    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = None

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
