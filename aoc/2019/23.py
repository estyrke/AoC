from io import StringIO, TextIOBase
import sys
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOBase):
    code = inp.read().strip()

    nodes = [Machine.from_str(code) for _ in range(50)]

    # Boot nodes with addresses
    for i, node in enumerate(nodes):
        node.run([i])

    queues: list[list[tuple[int, int]]] = [[] for _ in range(50)]
    while True:
        for i, node in enumerate(nodes):
            if queues[i]:
                x, y = queues[i].pop(0)
                output = node.run([x, y])
            else:
                output = node.run([-1])

            assert output is not None
            while len(output) >= 3:
                addr, x, y = output[:3]
                output = output[3:]
                if addr == 255:
                    return y
                queues[addr].append((x, y))


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    code = inp.read().strip()

    nodes = [Machine.from_str(code) for _ in range(50)]

    # Boot nodes with addresses
    for i, node in enumerate(nodes):
        node.run([i])

    queues: list[list[tuple[int, int]]] = [[] for _ in range(50)]
    nat = None
    last_nat = None
    while True:
        idle = True
        for i, node in enumerate(nodes):
            if queues[i]:
                idle = False
                x, y = queues[i].pop(0)
                output = node.run([x, y])
            else:
                output = node.run([-1])

            assert output is not None
            while len(output) >= 3:
                idle = False
                addr, x, y = output[:3]
                output = output[3:]
                if addr == 255:
                    nat = (x, y)
                else:
                    queues[addr].append((x, y))
        if idle and nat:
            print(nat)
            if last_nat is not None and last_nat == nat[1]:
                return last_nat
            last_nat = nat[1]
            queues[0].append(nat)


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
