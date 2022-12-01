import cProfile
from io import StringIO, TextIOWrapper
import math
import functools
import itertools
from typing import Iterable, List
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = None

    m = Machine.from_stream(inp)

    # print(m.disasm())
    outp = m.run()

    img = ascii(outp)
    print(img)

    img = img.splitlines()[:-1]

    answer = 0
    for y in range(1, len(img) - 1):
        for x in range(1, len(img[0]) - 1):
            if (
                img[y][x]
                == img[y - 1][x]
                == img[y + 1][x]
                == img[y][x - 1]
                == img[y][x + 1]
                == "#"
            ):
                answer += y * x
    return answer


def ascii(outp):
    return "".join(map(chr, outp))


def to_ascii(s: str) -> Iterable[int]:
    return map(ord, s)


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    m = Machine.from_stream(inp)
    m.memory[0] = 2

    score = 0
    A = "L,12,L,12,R,12\n"
    B = "L,8,L,8,R,12,L,8,L,8\n"
    C = "L,10,R,8,R,12\n"
    main = "A,A,B,C,C,A,B,C,A,B\n"

    print(ascii(m.run([])))
    print(ascii(m.run(to_ascii(main))))
    print(ascii(m.run(to_ascii(A))))
    print(ascii(m.run(to_ascii(B))))
    print(ascii(m.run(to_ascii(C))))

    b = StringIO()
    answer = None
    prev = None

    def printer(x):
        nonlocal b, prev, answer
        if x > 255:
            answer = x
            return

        if prev == x == 10:
            print(b.getvalue()[:-1], end="")
            b = StringIO()
        else:
            b.write(chr(x))

        prev = x

    m.run(to_ascii("y\n"), output_callback=printer)
    assert m.halted
    return answer

    # Decompress board (RLE compressed at 1182)
    board = []
    var_10 = 0
    for i in range(1182, 1533):
        var_9 = m.memory[i]
        for j in range(var_9):
            board.append(var_10)
        var_10 = int(var_10 == 0)

    scaffolds_visited = 0
    for y_pos in range(65):
        for x_pos in range(47):
            if board[y_pos * 47 + x_pos] == 1:
                scaffolds_visited += 1
                board_ptr = 1533 + y_pos * 47 + x_pos
                score += board_ptr + x_pos * y_pos + scaffolds_visited

    # print(m.disasm())

    return score
