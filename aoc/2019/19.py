from io import StringIO, TextIOBase
import logging
import sys
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOBase):
    logging.basicConfig(level=logging.INFO, force=True)
    answer = 0

    prog = inp.read()
    for y in range(50):
        for x in range(50):
            m2 = Machine.from_str(prog)
            outp = m2.run([x, y])
            assert outp and len(outp) == 1
            answer += outp[0]
            # raise RuntimeError()
            print("#" if outp[0] else ".", end="")
        print()

    return answer


part2_test_input = part1_test_input

part2_test_output = 250020


def part2(inp: TextIOBase):
    logging.basicConfig(level=logging.INFO, force=True)

    if IS_TEST:
        side = 10
    else:
        side = 100

    prog = inp.read()
    y = 6
    min_x = 0
    widths = {}
    while True:
        x = min_x
        outp = 0
        while True:
            m2 = Machine.from_str(prog)
            new_outp = m2.run([x, y])[0]
            # print(f"y={y}, x={x}, outp={new_outp}")

            if outp == 0 and new_outp == 1:
                min_x = x
                prev_min, prev_max = widths.get(y - 1, (0, 2))
                x += prev_max - prev_min - 2
            elif outp == 1 and new_outp == 0:
                max_x = x
                break
            outp = new_outp
            x += 1
        widths[y] = (min_x, max_x)
        print(f"y={y}, min_x={min_x}, max_x={max_x} width={max_x - min_x}")
        # if y > 10:
        #    return None

        old = widths.get(y - side + 1)
        if old:
            old_min, old_max = old
            if old_max - min_x >= side:
                return min_x * 10000 + y - side + 1

        y += 1


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
