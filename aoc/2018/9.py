from collections import deque
from io import StringIO, TextIOBase
import sys

part1_test_input = """9 players; last marble is worth 25 points"""
part1_test_output = 32


def part1(inp: TextIOBase):
    tokens = inp.read().split()
    players = int(tokens[0])
    last_marble = int(tokens[-2])

    circle = deque([0])
    scores = [0] * players
    player = 0

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.popleft()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

        player = (player + 1) % players

    return max(scores)


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    tokens = inp.read().split()
    players = int(tokens[0])
    last_marble = int(tokens[-2]) * 100

    circle = deque([0])
    scores = [0] * players
    player = 0

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.popleft()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

        player = (player + 1) % players

    return max(scores)


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
