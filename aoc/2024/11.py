from io import StringIO, TextIOBase
import sys

part1_test_input = """125 17"""

part1_test_output = 55312


def part1(inp: TextIOBase):
    answer = None

    stones = [int(x) for x in inp.read().strip().split()]

    for _ in range(25):
        new_stones = []
        # print(stones)
        for i, stone in enumerate(stones):
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                split_stones = [int(s[: len(s) // 2]), int(s[len(s) // 2 :])]
                new_stones.extend(split_stones)
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return len(stones)


part2_test_input = []

part2_test_output = None

table = {}


def extend_length(stone: int, blinks: int):
    if (stone, blinks) not in table:
        if blinks == 0:
            table[(stone, blinks)] = 1
        elif stone == 0:
            table[(stone, blinks)] = extend_length(1, blinks - 1)
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            s1, s2 = int(s[: len(s) // 2]), int(s[len(s) // 2 :])
            table[(stone, blinks)] = extend_length(s1, blinks - 1) + extend_length(s2, blinks - 1)

        else:
            table[(stone, blinks)] = extend_length(stone * 2024, blinks - 1)
    return table[(stone, blinks)]


def part2(inp: TextIOBase):
    stones = [int(x) for x in inp.read().strip().split()]

    answer = 0
    for stone in stones:
        res = extend_length(stone, 75)
        answer += res
    assert answer != 178223397238736
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
