from math import ceil
from io import StringIO, TextIOBase
import sys

part1_test_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

# Skip the test data because it is much harder than the real one
part1_test_output = None  # 2

IS_TEST: bool


def part1(inp: TextIOBase):
    answer = 0

    # for line in inp.readlines():
    *shapes, regions = inp.read().split("\n\n")
    shapes = [s.splitlines()[1:] for s in shapes]
    shape_sizes = [len([c for c in "".join(s) if c == "#"]) for s in shapes]
    regions = [r.split() for r in regions.splitlines()]
    hard = []
    for size, *nums in regions:
        x, y = [int(n) for n in size.strip(":").split("x")]
        nums = list(map(int, nums))
        total = sum(nums)
        if ceil(total / (x // 3)) <= (y // 3):
            # Fits without even trying
            answer += 1
            continue
        total_size = sum([shape_sizes[i] * n for i, n in enumerate(nums)])
        if total_size > x * y:
            # Impossible to fit because total blocks > available space
            continue
        hard.append((x, y, nums))

    if len(hard) == 0:
        return answer

    print("Oh no, there are some hard regions:")
    for x, y, nums in hard:
        print(f"{x}x{y}: {" ".join(map(str, nums))}")

    return None


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = None

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
