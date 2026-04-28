from io import StringIO, TextIOBase
import sys

part1_test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

part1_test_output = 3


def part1(inp: TextIOBase):
    answer = 0

    ranges, ids = inp.read().strip().split("\n\n")
    ranges = ranges.strip().split("\n")
    ids = ids.strip().split("\n")
    ranges = [r.split("-") for r in ranges]
    ranges = [tuple(int(i) for i in r) for r in ranges]
    ids = [int(i) for i in ids]

    for i in ids:
        for s, e in ranges:
            if i >= s and i <= e:
                answer += 1
                break

    return answer


part2_test_input = part1_test_input

part2_test_output = 14


def part2(inp: TextIOBase):
    answer = 0

    ranges, _ = inp.read().strip().split("\n\n")
    ranges = ranges.strip().split("\n")
    ranges = [r.split("-") for r in ranges]
    ranges = [tuple(int(i) for i in r) for r in ranges]

    ranges.sort()

    new_r = [ranges[0]]
    for r in ranges[1:]:
        assert r[0] <= r[1]
        if r[0] <= new_r[-1][1] + 1:
            new_r[-1] = (new_r[-1][0], max(new_r[-1][1], r[1]))
        else:
            new_r.append(r)

    ranges = new_r
    for s, e in ranges:
        answer += e - s + 1

    assert answer != 350774409766790
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
