from io import StringIO, TextIOWrapper
import sys

part1_test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

part1_test_output = 18


def check_pos(lines, x, y):
    res = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue

            res += check_dir(lines, x, y, dy, dx)
    return res


def check_dir(lines, x, y, dy, dx):
    word = "XMAS"
    for i in range(0, len(word)):
        if not 0 <= x + dx * i < len(lines[0]) or not 0 <= y + dy * i < len(lines):
            return 0
        if lines[y + dy * i][x + dx * i] != word[i]:
            return 0
    return 1


def part1(inp: TextIOWrapper):
    answer = 0

    lines = [list(l.strip()) for l in inp.readlines()]

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            answer += check_pos(lines, x, y)

    return answer


part2_test_input = part1_test_input

part2_test_output = 9


def part2(inp: TextIOWrapper):
    answer = 0
    lines = [list(l.strip()) for l in inp.readlines()]

    for y in range(1, len(lines) - 1):
        for x in range(1, len(lines[0]) - 1):
            answer += check_pos2(lines, x, y)
    return answer


def check_pos2(lines, x, y):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if lines[y][x] != "A":
            continue
        if (
            dy == 0
            and lines[y - 1][x + dx] == "M"
            and lines[y + 1][x + dx] == "M"
            and lines[y + 1][x - dx] == "S"
            and lines[y - 1][x - dx] == "S"
        ):
            return 1
        if (
            dx == 0
            and lines[y + dy][x + 1] == "M"
            and lines[y + dy][x - 1] == "M"
            and lines[y - dy][x - 1] == "S"
            and lines[y - dy][x + 1] == "S"
        ):
            return 1
    return 0


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
