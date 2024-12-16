from io import StringIO, TextIOBase
import sys

part1_test_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

part1_test_output = 10092


def part1(inp: TextIOBase):
    answer = None

    map, moves = inp.read().split("\n\n")
    map = [list(row) for row in map.strip().split("\n")]
    moves = moves.strip().replace("\n", "")
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "@":
                pos = (x, y)
                break
    print("\n".join(["".join(l) for l in map]))
    print(moves)

    for move in moves:
        if move == "<":
            dx, dy = -1, 0
        elif move == ">":
            dx, dy = 1, 0
        elif move == "^":
            dx, dy = 0, -1
        elif move == "v":
            dx, dy = 0, 1
        else:
            raise ValueError(f"Invalid move {move}")
        check_pos = (pos[0] + dx, pos[1] + dy)
        while map[check_pos[1]][check_pos[0]] == "O":
            check_pos = (check_pos[0] + dx, check_pos[1] + dy)

        if map[check_pos[1]][check_pos[0]] == "#":
            continue
        else:
            assert map[check_pos[1]][check_pos[0]] == "."
            while check_pos != pos:
                map[check_pos[1]][check_pos[0]] = "O"
                check_pos = (check_pos[0] - dx, check_pos[1] - dy)
            pos = pos[0] + dx, pos[1] + dy
            map[pos[1]][pos[0]] = "@"
            map[pos[1] - dy][pos[0] - dx] = "."
        # print("\n".join(["".join(l) for l in map]))

    answer = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "O":
                answer += 100 * y + x
    return answer


part2_test_input = part1_test_input

part2_test_output = 9021


def part2(inp: TextIOBase):
    map_in, moves = inp.read().split("\n\n")
    map_in = [list(row) for row in map_in.strip().split("\n")]
    moves = moves.strip().replace("\n", "")
    map = [[] for _ in range(len(map_in))]
    for y, row in enumerate(map_in):
        for x, cell in enumerate(row):
            if cell == "@":
                pos = (x * 2, y)
                map[y].extend("@.")
            elif cell == "#":
                map[y].extend("##")
            elif cell == "O":
                map[y].extend("[]")
            else:
                assert cell == "."
                map[y].extend("..")
    # print("\n".join(["".join(l) for l in map]))
    # print(moves)

    for m, move in enumerate(moves):
        # print("\n".join(["".join(l) for l in map]))
        # print(m, move)

        if move == "<":
            dx, dy = -1, 0
        elif move == ">":
            dx, dy = 1, 0
        elif move == "^":
            dx, dy = 0, -1
        elif move == "v":
            dx, dy = 0, 1
        else:
            raise ValueError(f"Invalid move {move}")

        if dy == 0:
            check_pos_x = (pos[0] + dx, pos[1] + dy)
            while map[check_pos_x[1]][check_pos_x[0]] in "[]":
                check_pos_x = (check_pos_x[0] + dx, check_pos_x[1] + dy)

            if map[check_pos_x[1]][check_pos_x[0]] == "#":
                continue
            else:
                assert map[check_pos_x[1]][check_pos_x[0]] == ".", f"Invalid cell {map[check_pos_x[1]][check_pos_x[0]]}"
                while check_pos_x != pos:
                    map[check_pos_x[1]][check_pos_x[0]] = map[check_pos_x[1] - dy][check_pos_x[0] - dx]
                    check_pos_x = (check_pos_x[0] - dx, check_pos_x[1] - dy)
                map[pos[1]][pos[0]] = "."
                pos = pos[0] + dx, pos[1] + dy

            continue

        # Now do the y movement
        check_pos: dict[int, set[int]] = {pos[1]: set([pos[0]])}
        new_y = pos[1]
        while True:
            new_cp = check_pos[new_y].copy()
            new_y += dy
            blocked = False
            free = True
            for cp in new_cp.copy():
                if map[new_y][cp] == "]":
                    new_cp.add(cp - 1)
                    free = False
                elif map[new_y][cp] == "[":
                    new_cp.add(cp + 1)
                    free = False
                elif map[new_y][cp] == "#":
                    blocked = True
                    free = False
                    break
                else:
                    if map[new_y][cp] != ".":
                        print(f"Invalid cell {map[new_y][cp]} at {cp}, {new_y}")
                    assert map[new_y][cp] == ".", f"Invalid cell {map[new_y][cp]}"
                    new_cp.remove(cp)

            if blocked:
                break

            check_pos[new_y] = new_cp
            if free:
                check_y = new_y
                while check_y in check_pos:
                    check_row = check_pos[check_y]
                    for check_x in check_row:
                        map[check_y + dy][check_x] = map[check_y][check_x]
                        map[check_y][check_x] = "."
                    check_y -= dy
                pos = pos[0], pos[1] + dy
                break

    answer = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "[":
                answer += 100 * y + x
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
