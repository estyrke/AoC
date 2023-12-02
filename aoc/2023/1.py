from io import TextIOWrapper
from pprint import pprint
import re

part1_test_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

part1_test_output = 142

repl = [
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9"),
]


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        nums = [x for x in line if "0" <= x <= "9"]
        answer += int(nums[0]) * 10 + int(nums[-1])
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

part2_test_output = 281

repl2 = dict(repl)
pprint(repl2)


def sub_num(x):
    r = repl2[x.group(0)]
    # print(f"{x} -> {r}")
    return r


def sub_numr(x):
    r = repl2[x.group(0)[::-1]]
    # print(f"{x} -> {r}")
    return r


def part2(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        line1 = re.sub("|".join(["(" + x[0] + ")" for x in repl]), sub_num, line, 1)
        line2 = re.sub(
            "|".join(["(" + x[0][::-1] + ")" for x in repl]), sub_numr, line[::-1], 1
        )[::-1]
        print(line, end="")

        # line = line.replace(src, dst)
        nums1 = [x for x in line1 if "0" <= x <= "9"]
        nums2 = [x for x in line2 if "0" <= x <= "9"]
        answer += int(nums1[0]) * 10 + int(nums2[-1])

    # return None
    assert answer not in [53896]
    # assert answer == 281
    return answer
