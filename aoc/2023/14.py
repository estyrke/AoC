from io import StringIO, TextIOWrapper
import sys

part1_test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

part1_test_output = 136


def part1(inp: TextIOWrapper):
    answer = 0

    lines = [list(l.strip()) for l in inp.readlines()]

    limits = [0] * len(lines[0])

    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                answer += len(lines) - limits[x]
                limits[x] += 1
            elif c == "#":
                limits[x] = y + 1

    return answer


part2_test_input = part1_test_input

part2_test_output = 64


def pprint(lines):
    for l in lines:
        print("".join(l))


def part2(inp: TextIOWrapper):
    answer = 0

    lines = [list(l.strip()) for l in inp.readlines()]

    cycles = 1_000_000_000
    moving = set()
    fixed = set()
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == "O":
                moving.add((x, y))
            elif c == "#":
                fixed.add((x, y))

    history = [lines]
    for i in range(cycles):
        new_lines = [[c for c in l] for l in lines]
        # North
        limits = [0] * len(lines)
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if new_lines[y][x] == "O":
                    new_lines[y][x] = "."
                    new_lines[limits[x]][x] = "O"
                    limits[x] += 1
                elif new_lines[y][x] == "#":
                    new_lines[y][x] = "#"
                    limits[x] = y + 1
                else:
                    assert new_lines[y][x] == "."
                    new_lines[y][x] = new_lines[y][x]

        # West
        limits = [0] * len(lines)
        for x in range(len(lines[0])):
            for y in range(len(lines)):
                if new_lines[y][x] == "O":
                    new_lines[y][x] = "."
                    new_lines[y][limits[y]] = "O"
                    limits[y] += 1
                elif new_lines[y][x] == "#":
                    new_lines[y][x] = "#"
                    limits[y] = x + 1
                else:
                    assert new_lines[y][x] == "."

        # South
        limits = [len(lines) - 1] * len(lines)
        for y in range(len(lines) - 1, -1, -1):
            for x in range(len(lines[0])):
                if new_lines[y][x] == "O":
                    new_lines[y][x] = "."
                    new_lines[limits[x]][x] = "O"
                    limits[x] -= 1
                elif new_lines[y][x] == "#":
                    new_lines[y][x] = "#"
                    limits[x] = y - 1
                else:
                    assert new_lines[y][x] == "."
                    new_lines[y][x] = new_lines[y][x]

        # East
        limits = [len(lines) - 1] * len(lines)
        for x in range(len(lines[0]) - 1, -1, -1):
            for y in range(len(lines)):
                if new_lines[y][x] == "O":
                    new_lines[y][x] = "."
                    new_lines[y][limits[y]] = "O"
                    limits[y] -= 1
                elif new_lines[y][x] == "#":
                    new_lines[y][x] = "#"
                    limits[y] = x - 1
                else:
                    assert new_lines[y][x] == "."

        if new_lines in history:
            index = history.index(new_lines)
            final_conf = reduce_cycles(cycles, i, index) - 1

            answer = sum(
                [
                    (len(lines) - y) * sum([1 if c == "O" else 0 for c in line])
                    for y, line in enumerate(history[final_conf])
                ]
            )
            break

        history.append(new_lines)
        lines = new_lines
        if i > 0 and i % 1000 == 0:
            print(i)
            print("Error! No loop found within limit! Try raising the limit.")
            break

    return answer


def reduce_cycles(cycles, i, index):
    return index + (cycles - index + 1) % (i - index + 1)


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
