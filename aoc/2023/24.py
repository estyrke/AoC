from io import StringIO, TextIOWrapper
from itertools import combinations
import sys

from aoc.tools import parse_input
from z3 import Int, Ints, Solver, Or

part1_test_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

part1_test_output = 2

IS_TEST: bool


def part1(inp: TextIOWrapper):
    answer = 0

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    stones = []
    for tokens in parse_input(inp, "{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}"):
        px, py, pz, vx, vy, vz = tokens
        stones.append(tokens)

    if IS_TEST:  # noqa: F821
        test_min, test_max = 7, 27
    else:
        test_min, test_max = (200000000000000, 400000000000000)

    for s1, s2 in combinations(stones, 2):
        (px1, py1, _pz1, vx1, vy1, _vz1), (px2, py2, _pz2, vx2, vy2, _vz2) = s1, s2
        den = (px1 - (px1 + vx1)) * (py2 - (py2 + vy2)) - (py1 - (py1 + vy1)) * (
            px2 - (px2 + vx2)
        )

        if den == 0:
            # trajectories are parallel
            continue

        ix = (
            (px1 * (py1 + vy1) - py1 * (px1 + vx1)) * (px2 - (px2 + vx2))
            - (px1 - (px1 + vx1)) * (px2 * (py2 + vy2) - py2 * (px2 + vx2))
        ) / den
        iy = (
            (px1 * (py1 + vy1) - py1 * (px1 + vx1)) * (py2 - (py2 + vy2))
            - (py1 - (py1 + vy1)) * (px2 * (py2 + vy2) - py2 * (px2 + vx2))
        ) / den
        if test_min <= ix <= test_max and test_min <= iy <= test_max:
            if ((vx1 > 0 and ix >= px1) or (vx1 < 0 and ix <= px1)) and (
                (vx2 > 0 and ix >= px2) or (vx2 < 0 and ix <= px2)
            ):
                answer += 1
            elif ((vy1 > 0 and iy >= py1) or (vy1 < 0 and iy <= py1)) and (
                (vy2 > 0 and iy >= py2) or (vy2 < 0 and iy <= py2)
            ):
                answer += 1
            else:
                assert abs(vx1) + abs(vy1) > 0
                # Intersection is in the past
        else:
            # Intersection is outside test area
            pass

    return answer


part2_test_input = part1_test_input

part2_test_output = 47


def part2(inp: TextIOWrapper):
    stones = []
    x0, y0, z0 = Ints("x0 y0 z0")
    vx0, vy0, vz0 = Ints("vx0 vy0 vz0")
    solver = Solver()
    lines = list(parse_input(inp, "{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}"))
    for i, tokens in enumerate(lines):
        px, py, pz, vx, vy, vz = tokens
        stones.append(tokens)

        t = Int(f"t{i+1}")
        solver.add(t > 0)

        solver.add(
            px + vx * t == x0 + vx0 * t,
            py + vy * t == y0 + vy0 * t,
            pz + vz * t == z0 + vz0 * t,
        )

        # Add some sanity checks.  I feel these shouldn't be needed, but without them the solver fails.
        if vx >= 0:
            solver.add(Or(vx0 >= vx, x0 >= px))
        else:
            solver.add(Or(vx0 <= vx, x0 <= px))
        if vy >= 0:
            solver.add(Or(vy0 >= vy, y0 >= py))
        else:
            solver.add(Or(vy0 <= vy, y0 <= py))
        if vz >= 0:
            solver.add(Or(vz0 >= vz, z0 >= pz))
        else:
            solver.add(Or(vz0 <= vz, z0 <= pz))

    assert str(solver.check()) == "sat"
    model = solver.model()

    x_s = model[x0].as_long()  # type: ignore
    y_s = model[y0].as_long()  # type: ignore
    z_s = model[z0].as_long()  # type: ignore
    # print(x_s, y_s, z_s)
    return x_s + y_s + z_s


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
