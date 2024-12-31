from io import StringIO, TextIOBase
import sys
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def print_ascii(out):
    print("".join(chr(c) if c < 256 else str(c) for c in out))


def part1(inp: TextIOBase):
    m = Machine.from_stream(inp)
    for line in [
        "NOT A J",  # If A is a hole, jump
        "NOT B T",  # If B is a hole, set T
        "OR T J",  # If A or B, jump
        "NOT C T",  # If C is a hole, set T
        "OR T J",  # If A or B or C, jump
        "AND D J",  # If jump and D is ground, jump
        "WALK",
    ]:
        print(line)
        out = m.run([ord(x) for x in line + "\n"])
        print_ascii(out)
        if m.halted:
            break

    if out and out[-1] > 256:
        return out[-1]
    return None


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    instr = inp.read()
    # with Path("aoc/2019/21_input.asm").open("w") as f:
    #    print(m.disasm(), file=f)
    # return None
    #  #.############  1  NOT A
    #  ##.###########  ?
    #  ###.##########  ?
    #  ####.#########  0
    #
    #  ##..#.########  1  NOT B AND NOT C AND NOT E
    #  ###..#.#######  0  NOT C AND D
    #  ####..#.######  0
    #   ABCDEFGHI
    #
    #  ###.#..#######  1  NOT C AND NOT E AND NOT F
    #  ####.#..######  0
    #   ABCDEFGHI
    #
    #  #.#.#..##.####  1
    #  ##.#.#..##.###  0
    #  ###.#.#..##.##  0  NOT C AND D AND (E OR H)
    #  ####.#.#..##.#  0
    #   ABCDEFGHI
    #
    #  #..####..#####  1
    #  ##..####..####  ?
    #  ###..####..###  0
    #  ####..####..##  0
    #   ABCDEFGHI

    #  ##.##.########  1  NOT B AND NOT E
    #  ###.##.#######  ?
    #  ####.##.######  0
    #   ABCDEFGHI

    #  #.####.#..####
    #  ##.####.#..###  1  NOT B AND NOT G AND NOT I
    #  ###.####.#..##  1
    #   ABCDEFGHI

    #
    # (NOT C AND NOT E AND NOT F) OR (NOT B AND NOT C AND NOT E) OR NOT A
    # (NOT (C OR E OR F)) OR (NOT (B OR C OR E)) OR NOT A
    # NOT X OR NOT Y OR NOT Z => NOT (X AND Y AND Z)
    # NOT ((C OR E OR F) AND (B OR C OR E) AND A)
    # If C is a hole and D is ground -> jump
    # else if A is a hole -> jump
    # else if B is a hole and E is a hole -> jump

    temp = [
        "OR C T",
        "OR E T",
        "OR F T",
        "OR B J",
        "OR C J",
        "OR E J",
        "AND T J",
        "AND A J",
        "NOT J J",
        "RUN",
    ]

    # D AND ((NOT C AND (E OR H)) OR (NOT B AND NOT E) OR NOT A)
    # D AND (NOT (C OR NOT (E OR H)) OR NOT (B OR E) OR NOT A)
    # D AND NOT ((C OR NOT (E OR H)) AND (B OR E) AND A)
    # D AND (NOT (C OR (B AND E)) OR (E AND H) OR NOT A)
    temp = [
        "OR E J",
        "OR H J",
        "NOT J J",
        "OR C J",
        "OR B T",
        "OR E T",
        "AND T J",
        "AND A J",
        "NOT J J",
        "AND D J",
        "RUN",
    ]

    return test_program(Machine.from_str(instr), temp)


def test_program(m: Machine, prog: list[str]):
    for line in prog:
        print(line)
        out = m.run([ord(x) for x in line + "\n"])
        print_ascii(out)
        if m.halted:
            break

    if out and out[-1] > 256:
        return out[-1]
    return None


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
