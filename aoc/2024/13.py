from io import StringIO, TextIOBase
import sys

part1_test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

part1_test_output = 480


def part1(inp: TextIOBase):
    answer = 0

    lines = inp.readlines()
    for i in range(0, len(lines), 4):
        a = lines[i].split()
        b = lines[i + 1].split()
        p = lines[i + 2].split()

        ax, ay = [int(x[2:].rstrip(",")) for x in a[2:4]]
        bx, by = [int(x[2:].rstrip(",")) for x in b[2:4]]
        px, py = [int(x[2:].rstrip(",")) for x in p[1:3]]

        print(ax, ay, bx, by, px, py)
        # a*ax + b*bx = px
        # a*ay + b*by = py
        b = min(px // bx, py // by, 100)
        best = None
        while b >= 0:
            if (px - b * bx) % ax == 0 and (py - b * by) % ay == 0:
                a = (px - b * bx) // ax
                if a >= 0 and a * ay + b * by == py:
                    best = min(best or 400, a * 3 + b)
            b -= 1

        if best is not None:
            answer += best

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = 0

    lines = inp.readlines()
    for i in range(0, len(lines), 4):
        a = lines[i].split()
        b = lines[i + 1].split()
        p = lines[i + 2].split()

        ax, ay = [int(x[2:].rstrip(",")) for x in a[2:4]]
        bx, by = [int(x[2:].rstrip(",")) for x in b[2:4]]
        px, py = [int(x[2:].rstrip(",")) + 10_000_000_000_000 for x in p[1:3]]

        # a*ax + b*bx = px
        # a*ay + b*by = py

        # (ax bx) (a) = (px)
        # (ay by) (b) = (py)

        # (1 bx/ax) (a) = (px/ax)
        # (0  by-ay*(bx/ax)) (b) = (py-ay*(px/ax))

        # (1 bx/ax) (a) = (px/ax)
        # (0 1) (b) = (py-ay*(px/ax))/(by-ay*(bx/ax))

        b = round((py - ay * px / ax) / (by - ay * bx / ax))
        a = round((px / ax) - b * bx / ax)

        if b * by + a * ay == py and b * bx + a * ax == px:
            answer += a * 3 + b

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
