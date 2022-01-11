from io import TextIOWrapper
import math
import functools
import itertools
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = None

    m = Machine.from_stream(inp)

    # print(m.disasm())
    outp = m.run()

    img = "".join(map(chr, outp))
    # print(img)

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


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    m = Machine.from_stream(inp)
    m.memory[0] = 2
    score = 0

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

    print(m.disasm())

    return score
