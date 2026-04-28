from functools import cache
from io import StringIO, TextIOBase
import sys

part1_test_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

part1_test_output = 21


def part1(inp: TextIOBase):
    answer = 0


    # for line in inp.readlines():
    lines = [l.strip() for l in inp.readlines()]
    beams = set()
    for line in lines:
        if not beams:
             beams.add(line.index("S"))
             continue
        for i, ch in enumerate(line):
            if ch == "^":
                if i in beams:
                    beams.remove(i)
                    if i > 0:
                        beams.add(i-1)
                    if i < len(line) - 1:
                        beams.add(i+1)
                    answer += 1

    return answer


part2_test_input = part1_test_input

part2_test_output = 40

lines: list[str]

@cache
def timelines(y: int, beam: int) -> int:
    global lines
    if y >= len(lines):
        return 1

    if lines[y][beam] == "^":
        tl = 0
        if beam > 0:
            tl += timelines(y+1, beam - 1)
        if beam < len(lines[0]) - 1:
            tl += timelines(y+1, beam + 1)
        return tl
    return timelines(y+1, beam)

def part2(inp: TextIOBase):
    answer = 0
    global lines

    # for line in inp.readlines():
    lines = [l.strip() for l in inp.readlines()]

    answer = timelines(1, lines[0].index("S"))


    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
