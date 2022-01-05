from io import TextIOWrapper
import math
import functools
import itertools
from typing import Dict, List, Tuple
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None

code = """
      x = 21
      x_is_odd = 1
      y = 21
      y_is_odd = 1
      y_half = 10
while True:
    inp direction
    if direction == 1: # North
        new_x = x
        new_x_is_odd = x_is_odd
        new_y = y - 1
        new_y_is_odd = not y_is_odd
        new_y_half = y_half -new_y_is_odd
    elif direction == 2: # South
        new_x = x
        new_x_is_odd = x_is_odd
        new_y = y + 1
        new_y_is_odd = not y_is_odd
        new_y_half = y_half + y_is_odd
    elif direction == 3: # West
        new_x = x - 1
        new_x_is_odd = not x_is_odd
        new_y = y
        new_y_is_odd = y_is_odd
        new_y_half = y_half
    elif direction == 4: # East
        new_x = x + 1
        new_x_is_odd = not x_is_odd
        new_y = y
        new_y_is_odd = y_is_odd
        new_y_half = y_half
    else:
        stop

    if new_x != 0 and new_y != 0 and new_x != 40 and new_y != 40:
        if new_x == 35 and new_y == 1
            result = 2
        elif new_x_is_odd and new_y_is_odd:
            result = 1
        elif not new_x_is_odd and not new_y_is_odd:
            result = 0
        else:
            a = (new_y_half + new_y_is_odd - 1) * 39 + new_x - 1
            result = int(mem[252 + a] < 71)
    else:
        result = 0

    if result != 0:
        x = new_x
        y = new_y
        x_is_odd = new_x_is_odd
        y_is_odd = new_y_is_odd
        y_half = new_y_half

    outp result

  252 data 63, 79, 32, 16, 21, 23, 90, 91
  260 data 50, 57, 98, 31, 96, 21, 59, 30
  268 data 88, 68, 89, 15, 28, 86, 14, 75
  276 data 41, 29, 86, 04, 80, 51, 46, 48
  284 data 68, 93, 74, 17, 76, 18, 32, 36
  292 data 80, 02, 77, 80, 09, 98, 38, 82
  300 data 65, 93, 76, 29, 23, 89, 97, 13
  308 data 75, 35, 02, 91, 73, 86, 69, 90
  316 data 09, 78, 84, 06, 16, 98, 97, 91
  324 data 66, 41, 99, 56, 35, 78, 15, 85
  332 data 67, 77, 55, 96, 59, 20, 88, 24
  340 data 80, 48, 85, 79, 92, 23, 68, 67
  348 data 99, 98, 96, 57, 20, 32, 90, 20
  356 data 06, 79, 33, 97, 21, 58, 90, 41
  364 data 83, 83, 07, 64, 14, 08, 92, 59
  372 data 83, 13, 96, 95, 51, 89, 41, 72
  380 data 51, 82, 60, 34, 81, 56, 77, 10
  388 data 04, 14, 61, 74, 94, 87, 03, 86
  396 data 52, 84, 92, 35, 88, 28, 78, 17
  404 data 57, 72, 85, 67, 56, 82, 83, 54
  412 data 89, 33, 04, 84, 03, 66, 45, 85
  420 data 16, 22, 74, 94, 75, 57, 68, 80
  428 data 86, 94, 18, 27, 53, 90, 72, 38
  436 data 95, 34, 20, 99, 98, 40, 95, 93
  444 data 55, 46, 07, 29, 87, 32, 56, 21
  452 data 98, 30, 88, 95, 77, 24, 73, 95
  460 data 14, 85, 02, 66, 73, 30, 85, 08
  468 data 69, 78, 75, 93, 04, 76, 56, 51
  476 data 89, 99, 51, 94, 14, 72, 39, 85
  484 data 96, 98, 37, 37, 75, 79, 61, 73
  492 data 96, 04, 97, 41, 92, 68, 58, 76
  500 data 29, 29, 78, 97, 44, 73, 67, 75
  508 data 85, 18, 01, 02, 09, 99, 10, 98
  516 data 19, 11, 73, 67, 86, 01, 94, 35
  524 data 29, 16, 99, 27, 35, 76, 42, 60
  532 data 99, 43, 28, 74, 11, 74, 91, 81
  540 data 11, 13, 91, 97, 75, 80, 68, 51
  548 data 81, 81, 77, 51, 72, 75, 59, 85
  556 data 62, 83, 91, 09, 20, 83, 57, 61
  564 data 31, 94, 80, 26, 52, 93, 86, 87
  572 data 78, 39, 46, 74, 86, 55, 24, 87
  580 data 95, 16, 82, 49, 75, 11, 73, 92
  588 data 64, 69, 43, 82, 41, 50, 24, 98
  596 data 08, 03, 73, 77, 19, 49, 99, 29
  604 data 96, 35, 86, 82, 60, 65, 36, 92
  612 data 89, 84, 69, 58, 95, 31, 67, 84
  620 data 44, 78, 24, 80, 46, 48, 98, 39
  628 data 94, 10, 78, 89, 95, 28, 82, 41
  636 data 97, 88, 23, 83, 67, 42, 97, 44
  644 data 78, 83, 28, 29, 66, 94, 45, 61
  652 data 37, 79, 55, 79, 30, 95, 45, 47
  660 data 76, 18, 84, 81, 93, 29, 90, 90
  668 data 86, 13, 86, 18, 47, 86, 87, 70
  676 data 01, 92, 98, 16, 70, 21, 54, 85
  684 data 54, 29, 73, 76, 80, 59, 84, 92
  692 data 16, 81, 87, 33, 96, 86, 29, 18
  700 data 84, 42, 60, 94, 67, 59, 89, 26
  708 data 42, 91, 42, 75, 58, 95, 81, 82
  716 data 38, 49, 85, 52, 43, 93, 90, 41
  724 data 88, 85, 12, 37, 77, 78, 95, 35
  732 data 87, 35, 35, 55, 92, 72, 26, 76
  740 data 19, 96, 19, 87, 66, 97, 81, 85
  748 data 58, 58, 74, 39, 74, 43, 51, 90
  756 data 48, 77, 56, 78, 16, 81, 57, 34
  764 data 95, 72, 18, 06, 75, 16, 61, 89
  772 data 56, 59, 76, 35, 18, 98, 76, 05
  780 data 75, 11, 86, 93, 51, 94, 06, 76
  788 data 84, 26, 82, 10, 29, 95, 74, 20
  796 data 74, 78, 05, 63, 14, 96, 84, 54
  804 data 55, 75, 85, 24, 95, 72, 54, 49
  812 data 92, 78, 22, 95, 97, 58, 70, 87
  820 data 28, 41, 88, 25, 75, 07, 29, 95
  828 data 67, 32, 82, 80, 81, 41, 63, 69
  836 data 56, 10, 81, 75, 08, 18, 94, 56
  844 data 67, 18, 83, 56, 64, 93, 84, 60
  852 data 73, 95, 13, 72, 04, 96, 97, 40
  860 data 77, 35, 62, 78, 77, 35, 73, 56
  868 data 99, 40, 64, 60, 90, 82, 86, 52
  876 data 89, 17, 21, 87, 84, 19, 92, 81
  884 data 92, 84, 81, 67, 73, 09, 26, 87
  892 data 02, 11, 76, 31, 72, 61, 89, 11
  900 data 78, 83, 67, 01, 64, 97, 82, 12
  908 data 73, 99, 81, 68, 58, 77, 15, 14
  916 data 31, 91, 76, 58, 17, 83, 45, 54
  924 data 77, 40, 47, 82, 40, 72, 73, 95
  932 data 10, 96, 29, 77, 21, 92, 87, 11
  940 data 55, 93, 87, 84, 08, 89, 51, 24
  948 data 87, 38, 97, 92, 48, 99, 08, 49
  956 data 78, 42, 91, 78, 50, 87, 89, 46
  964 data 80, 83, 25, 11, 74, 22, 81, 39
  972 data 99, 53, 93, 61, 93, 65, 83, 80
  980 data 35, 02, 85, 27, 33, 95, 24, 99
  988 data 86, 23, 89, 09, 26, 75, 66, 81
  996 data 29, 75, 20, 89, 08, 97, 17, 73
 1004 data 63, 82, 73, 90, 32, 92, 68, 82
 1012 data 59, 93, 48, 78, 67, 98, 34, 91
 1020 data 32, 82, 73, 74, 02, 77, 16, 90
 1028 data 61, 75, 30, 92, 00, 00, 21, 21
 1036 data 01, 10, 01, 00, 00, 00, 00, 00
 1044 data 00
 """


def part1(inp: TextIOWrapper):
    m = Machine.from_stream(inp)
    # print(m.disasm())

    board: List[List[int]] = [[-1] * 41 for _ in range(41)]

    for y in range(41):
        for x in range(41):
            if x == 0 or y == 0 or x == 40 or y == 40:
                board[y][x] = 0
            elif x % 2 == 1 and y % 2 == 1:
                board[y][x] = 1
            elif x % 2 == 0 and y % 2 == 0:
                board[y][x] = 0
            else:
                a = (y // 2 + (y % 2) - 1) * 39 + x - 1
                board[y][x] = int(m.memory[252 + a] < 71)

    # print_board(board, (21, 21), (35, 1))
    target_pos, _, map, min_path = make_map(m)

    print_map(map, target_pos)
    return min_path


def make_map(m: Machine):
    pos = (0, 0)
    direction = 3
    path = []
    map: Dict[Tuple[int, int], int] = {(0, 0): 1}
    min_path = -1
    target_pos = (-1, -1)
    target_dir = -1
    while not m.halted:
        for new_dir, new_pos in next_positions(pos, direction):
            if map.get(new_pos, None) in [0, 3]:
                continue  # blocked
            status = m.run([new_dir])[0]
            if status == 0:
                map[new_pos] = 0
            else:
                if status == 2:
                    target_pos, target_dir = new_pos, new_dir

                    min_path = len(path) + 1

                map[new_pos] = 1
                path.append((direction, pos))
                direction, pos = new_dir, new_pos
                break
        else:
            # Unable to proceed; backtrack
            map[pos] = 3
            if len(path) == 0:
                break
            status = m.run([back(direction)])[0]
            if status != 1:
                print_map(map, pos)
                print(path)
                print(direction, pos, back(direction))
            assert status == 1
            direction, pos = path.pop()

    return target_pos, target_dir, map, min_path


def print_board(board, pos, target):
    for y in range(41):
        for x in range(41):
            if (x, y) == pos:
                print("D", end="")
            elif (x, y) == target:
                print("X", end="")
            else:
                print(" " if board[y][x] == 1 else "#", end="")
        print()


def print_map(map, pos):
    min_x = min_y = 0
    for x, y in map.keys():
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    for y in range(41):
        for x in range(41):
            value = map.get((x + min_x, y + min_y), -1)
            if (x + min_x, y + min_y) == pos:
                print("D", end="")
            elif (x + min_x, y + min_y) == (0, 0):
                print("S", end="")
            elif value == -1:
                print("?", end="")
            elif value == 1:
                print(" ", end="")
            elif value == 3:
                print(".", end="")
            elif value == 4:
                print("O", end="")
            else:
                assert value == 0
                print("#", end="")
        print()


def next_positions(pos, direction):
    """
    >>> list(next_positions((4, 5), 1))
    [(4, (5, 5)), (1, (4, 4)), (3, (3, 5))]
    >>> list(next_positions((4, 5), 2))
    [(3, (3, 5)), (2, (4, 6)), (4, (5, 5))]
    >>> list(next_positions((4, 5), 3))
    [(1, (4, 4)), (3, (3, 5)), (2, (4, 6))]
    >>> list(next_positions((4, 5), 4))
    [(2, (4, 6)), (4, (5, 5)), (1, (4, 4))]
    """
    dir_map = {1: 0, 2: 2, 3: 3, 4: 1}
    positions = [
        (1, (pos[0], pos[1] - 1)),
        (4, (pos[0] + 1, pos[1])),
        (2, (pos[0], pos[1] + 1)),
        (3, (pos[0] - 1, pos[1])),
    ]

    yield positions[(dir_map[direction] + 1) % 4]  # Right turn
    yield positions[(dir_map[direction]) % 4]  # Straight
    yield positions[(dir_map[direction] - 1) % 4]  # Left turn


def back(direction):
    return {1: 2, 2: 1, 3: 4, 4: 3}[direction]


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    m = Machine.from_stream(inp)

    target_pos, target_dir, map, _ = make_map(m)

    oxygen = [(target_pos, back(target_dir))]
    for minute in itertools.count(1):
        next_oxygen = []
        for pos, dir in oxygen:
            for next_dir, next_pos in next_positions(pos, dir):
                if map[next_pos] == 3:
                    map[next_pos] = 4
                    next_oxygen.append((next_pos, next_dir))
        if len(next_oxygen) == 0:
            break
        oxygen = next_oxygen
        # print_map(map, target_pos)
        # input()
    return minute - 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
