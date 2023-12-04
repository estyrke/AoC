from collections import defaultdict
from io import TextIOWrapper

part1_test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

part1_test_output = 4361


def adjacent(lines, x, y):
    if x > 0:
        if y > 0 and lines[y - 1][x - 1] not in "0123456789.":
            return True
        if y < len(lines) - 1 and lines[y + 1][x - 1] not in "0123456789.":
            return True
        if lines[y][x - 1] not in "0123456789.":
            return True
    if x < len(lines[0]) - 1:
        if y > 0 and lines[y - 1][x + 1] not in "0123456789.":
            return True
        if y < len(lines) - 1 and lines[y + 1][x + 1] not in "0123456789.":
            return True
        if lines[y][x + 1] not in "0123456789.":
            return True
    if y > 0 and lines[y - 1][x] not in "0123456789.":
        return True
    if y < len(lines) - 1 and lines[y + 1][x] not in "0123456789.":
        return True
    return False


def part1(inp: TextIOWrapper):
    answer = 0

    # for line in inp.readlines():
    lines = [list(l.strip()) for l in inp.readlines()]

    for y, line in enumerate(lines):
        pn = 0
        adj = False
        for x, c in enumerate(line):
            if "0" <= c <= "9":
                pn *= 10
                pn += int(c)
                if adjacent(lines, x, y):
                    adj = True
            else:
                # print(adj, pn)
                if adj:
                    answer += pn
                pn = 0
                adj = False
        if adj:
            answer += pn
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = 467835


def gear(lines, x, y):
    gears = []
    if x > 0:
        if y > 0 and lines[y - 1][x - 1] == "*":
            gears.append((y - 1, x - 1))
        if y < len(lines) - 1 and lines[y + 1][x - 1] == "*":
            gears.append((y + 1, x - 1))
        if lines[y][x - 1] == "*":
            gears.append((y, x - 1))
    if x < len(lines[0]) - 1:
        if y > 0 and lines[y - 1][x + 1] == "*":
            gears.append((y - 1, x + 1))
        if y < len(lines) - 1 and lines[y + 1][x + 1] == "*":
            gears.append((y + 1, x + 1))
        if lines[y][x + 1] == "*":
            gears.append((y, x + 1))
    if y > 0 and lines[y - 1][x] == "*":
        gears.append((y - 1, x))
    if y < len(lines) - 1 and lines[y + 1][x] == "*":
        gears.append((y + 1, x))
    return gears


def part2(inp: TextIOWrapper):
    answer = 0

    lines = [list(l.strip()) for l in inp.readlines()]

    gears = defaultdict(list)
    for y, line in enumerate(lines):
        pn = 0
        adj = set()
        for x, c in enumerate(line):
            if "0" <= c <= "9":
                pn *= 10
                pn += int(c)
                for g in gear(lines, x, y):
                    adj.add(g)
            else:
                if pn in (742, 842):
                    print(lines[17][73])
                    print(gear(lines, x - 2, y))
                    print((y, x), adj, pn)
                for y2, x2 in adj:
                    gears[(y2, x2)].append(pn)
                pn = 0
                adj = set()
        if adj:
            for y2, x2 in adj:
                gears[(y2, x2)].append(pn)

    # pprint(gears)
    for (y, x), pns in gears.items():
        if len(pns) == 2:
            answer += pns[0] * pns[1]

    assert answer not in [14173608, 40902202]
    return answer
