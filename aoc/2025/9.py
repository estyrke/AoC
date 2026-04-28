from io import StringIO, TextIOBase
import sys
from shapely import Polygon

part1_test_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

part1_test_output = 50


def part1(inp: TextIOBase):
    reds = [l.strip().split(",") for l in inp.readlines()]
    reds = [(int(x[0]), int(x[1])) for x in reds]

    answer = 0
    for i, (x1, y1) in enumerate(reds):
        for j, (x2, y2) in enumerate(reds[i+1:], i+1):
            size = (abs(x1-x2)+1)*(abs(y1-y2)+1)
            if size > answer:
                answer = size
    return answer


part2_test_input = part1_test_input

part2_test_output = 24


def part2(inp: TextIOBase):
    reds = [l.strip().split(",") for l in inp.readlines()]
    reds = [(int(x[0]), int(x[1])) for x in reds]

    shell = Polygon([*reds, reds[0]])
    answer = 0
    for i, (x1, y1) in enumerate(reds):
        for j, (x2, y2) in enumerate(reds[i+1:], i+1):
            p = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            size = (abs(x1-x2)+1)*(abs(y1-y2)+1)
            size2 = p.area
            #assert size == size2, f"{size}, {size2}"
            if shell.contains(p) and size > answer:
                answer = size
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
