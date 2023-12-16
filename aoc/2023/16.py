from io import StringIO, TextIOWrapper
import sys

part1_test_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

part1_test_output = 46


def part1(inp: TextIOWrapper):
    lines = [l.strip() for l in inp.readlines()]
    beams: list[tuple[tuple[int, int], tuple[int, int]]] = [((0, 0), (1, 0))]

    return energize(lines, beams)


def energize(lines, beams):
    energized = {}

    while beams:
        bp, bd = beams.pop(0)
        if not 0 <= bp[0] < len(lines[0]) or not 0 <= bp[1] < len(lines):
            # outside
            continue
        if (bp, bd) in energized:
            # already travelled
            continue

        energized[(bp, bd)] = 1
        at = lines[bp[1]][bp[0]]
        if at == "." or (at == "-" and bd[1] == 0) or (at == "|" and bd[0] == 0):
            beams.append(((bp[0] + bd[0], bp[1] + bd[1]), bd))
        elif at == "\\":
            bd = bd[1], bd[0]
            beams.append(((bp[0] + bd[0], bp[1] + bd[1]), bd))
        elif at == "/":
            bd = -bd[1], -bd[0]
            beams.append(((bp[0] + bd[0], bp[1] + bd[1]), bd))
        elif at == "|":
            beams.append(((bp[0] + 0, bp[1] - 1), (0, -1)))
            beams.append(((bp[0] + 0, bp[1] + 1), (0, 1)))
        elif at == "-":
            beams.append(((bp[0] - 1, bp[1]), (-1, 0)))
            beams.append(((bp[0] + 1, bp[1]), (1, 0)))
        else:
            assert False

    return len(set(bp for bp, _ in energized))


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    lines = [l.strip() for l in inp.readlines()]

    answer = 0

    assert len(lines) == len(lines[0])
    for i in range(len(lines)):
        new_ans = energize(lines, [((i, 0), (0, 1))])
        answer = max(new_ans, answer)
        new_ans = energize(lines, [((i, len(lines) - 1), (0, -1))])
        answer = max(new_ans, answer)
        new_ans = energize(lines, [((0, i), (1, 0))])
        answer = max(new_ans, answer)
        new_ans = energize(lines, [((len(lines) - 1, i), (-1, 0))])
        answer = max(new_ans, answer)
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
