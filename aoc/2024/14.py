from io import StringIO, TextIOBase
import sys
from aoc.tools import parse_input

part1_test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

part1_test_output = 12
IS_TEST = 0


def part1(inp: TextIOBase):
    lines = [[int(t) for t in tokens] for tokens in parse_input(inp, r"p={},{} v={},{}")]
    if IS_TEST:
        w, h = 11, 7
    else:
        w, h = 101, 103

    nw = ne = sw = se = 0
    turns = 100
    for px, py, vx, vy in lines:
        new_px = (px + vx * turns) % w
        new_py = (py + vy * turns) % h
        if new_px < w // 2 and new_py < h // 2:
            nw += 1
        elif new_px < w // 2 and new_py > h // 2:
            sw += 1
        elif new_px > w // 2 and new_py < h // 2:
            ne += 1
        elif new_px > w // 2 and new_py > h // 2:
            se += 1

    print(nw, ne, sw, se)
    return nw * se * ne * sw


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    lines = [[int(t) for t in tokens] for tokens in parse_input(inp, r"p={},{} v={},{}")]

    if IS_TEST:
        w, h = 11, 7
        return None
    else:
        w, h = 101, 103

    for turns in range(100_000):
        if turns % 100000 == 0:
            print(turns)
        bots = {}
        for px, py, vx, vy in lines:
            new_px = (px + vx * turns) % w
            new_py = (py + vy * turns) % h
            bots[new_px, new_py] = True

        sym = 0
        for bot in bots:
            if bots.get((w - bot[0] - 1, bot[1]), False):
                sym += 1

        if sym > 100:
            print(chr(27) + "[2J")
            for y in range(h):
                for x in range(w):
                    if bots.get((x, y)):
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            print(turns)
            return turns


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
