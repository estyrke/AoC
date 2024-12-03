from io import StringIO, TextIOWrapper
import re
import sys

part1_test_input = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

part1_test_output = 161


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]
    matches = re.findall(r"mul\((\d+),(\d+)\)", inp.read())
    answer = sum(int(a) * int(b) for a, b in matches)

    return answer


part2_test_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

part2_test_output = 48


def part2(inp: TextIOWrapper):
    matches = re.findall(r"(don't)|(do)|(mul)\((\d+),(\d+)\)", inp.read())
    answer = 0
    do = True
    for match in matches:
        print(match)
        if match[1]:
            do = True
        elif match[0]:
            do = False
        elif match[2]:
            if do:
                answer += int(match[3]) * int(match[4])

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
