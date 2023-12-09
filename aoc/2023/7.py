from collections import defaultdict
from io import StringIO, TextIOWrapper
import sys

part1_test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

part1_test_output = 6440

cards = [""]

rank = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def part1(inp: TextIOWrapper):
    answer = None

    hands = []
    for line in inp.readlines():
        cards, bid = line.strip().split()
        cards = list(cards.strip())
        hand = defaultdict(int)
        for card in cards:
            hand[rank[card]] += 1
        s = [v for k, v in sorted(hand.items(), key=lambda c: (-c[1], -c[0]))] + [
            rank[card] for card in cards
        ]
        hands.append((s, int(bid)))

    hands.sort()
    answer = sum([(i + 1) * bid for i, (s, bid) in enumerate(hands)])
    return answer


part2_test_input = part1_test_input

part2_test_output = 5905

rank2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


def part2(inp: TextIOWrapper):
    answer = None

    hands = []
    for line in inp.readlines():
        cards, bid = line.strip().split()
        cards = list(cards.strip())
        hand = defaultdict(int)
        for card in cards:
            hand[rank2[card]] += 1
        types = [
            v for k, v in sorted(hand.items(), key=lambda c: (-c[1], -c[0])) if k != 1
        ]
        if len(types) == 0:
            types = [5]
        else:
            types[0] += hand[1]
        s = types + [rank2[card] for card in cards]
        hands.append((s, int(bid)))

    hands.sort()
    answer = sum([(i + 1) * bid for i, (s, bid) in enumerate(hands)])
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
