from collections import defaultdict
from io import TextIOWrapper

part1_test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

part1_test_output = 13


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        line2 = line.split(":")[1]
        winning, mine = line2.split("|")
        winning = set([int(x) for x in winning.strip().split()])
        mine = set([int(x) for x in mine.strip().split()])

        matches = len(winning & mine)
        if matches:
            answer += 2 ** (matches - 1)

    return answer


part2_test_input = part1_test_input

part2_test_output = 30


def part2(inp: TextIOWrapper):
    counts = defaultdict(int)
    for line in inp.readlines():
        id, line2 = line.split(":")
        id = int(id.split()[1])
        counts[id] += 1
        winning, mine = line2.split("|")
        winning = set([int(x) for x in winning.strip().split()])
        mine = set([int(x) for x in mine.strip().split()])

        matches = len(winning & mine)
        for down in range(matches):
            counts[id + down + 1] += counts[id]
    print(counts)
    return sum(counts.values())
