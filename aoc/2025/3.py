from io import StringIO, TextIOBase
import sys

part1_test_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

part1_test_output = 357


def part1(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        bats = [int(x) for x in line.strip()]
        jolts = 0
        for i, num1 in enumerate(bats[:-1]):
            if num1 < jolts // 10:
                continue
            num2 = max(bats[i + 1 :])
            if num1 * 10 + num2 > jolts:
                jolts = num1 * 10 + num2
        answer += jolts

    return answer


part2_test_input = part1_test_input

part2_test_output = 3121910778619


def part2(inp: TextIOBase):
    answer = 0
    num_bats = 12
    for line in inp.readlines():
        bats = [int(x) for x in line.strip()]
        jolts = 0
        for i in range(num_bats):
            limit = -num_bats + i + 1
            num = max(bats[: limit if limit != 0 else None])
            pos = bats.index(num)
            jolts = jolts * 10 + num
            bats = bats[pos + 1 :]
        answer += jolts

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
