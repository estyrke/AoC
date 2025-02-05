from io import StringIO, TextIOBase
import itertools
import sys

part1_test_input = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

part1_test_output = 12


def part1(inp: TextIOBase):
    threes = 0
    twos = 0
    for line in inp.readlines():
        counts = {}
        for char in line.strip():
            counts[char] = counts.get(char, 0) + 1
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1

    return twos * threes


part2_test_input = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""

part2_test_output = "fgij"


def part2(inp: TextIOBase):
    for a, b in itertools.combinations(inp.readlines(), 2):
        equal = [x for x, y in zip(a, b) if x == y]
        if len(equal) == len(a) - 1:
            return "".join(equal).strip()
    return None


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
