from io import StringIO, TextIOWrapper
import sys

part1_test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
68 70 71 69 72 74 71
"""

part1_test_output = 2


def find_fault(seq: list[int], debug=False):
    try:
        fault = None
        sign = (seq[1] - seq[0]) // abs(seq[1] - seq[0]) if seq[1] != seq[0] else 0
        if sign == 0:
            fault = 0
            return fault
        for i, prev, num in zip(range(len(seq) - 1), seq[:-1], seq[1:], strict=True):
            if sign == 1 and not prev + 1 <= num <= prev + 3:
                fault = i
                return fault
            if sign == -1 and not prev - 3 <= num <= prev - 1:
                fault = i
                return fault
    finally:
        if debug and fault is not None:
            for j, n in enumerate(seq):
                if j == fault:
                    print(f"({n})", end=" ")
                else:
                    print(n, end=" ")
            print(" (fault: ", fault, ")")
    return None


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        nums = [int(n) for n in line.split()]
        if find_fault(nums) is None:
            answer += 1

    return answer


part2_test_input = part1_test_input

part2_test_output = 4


def part2(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        nums = [int(n) for n in line.split()]
        if (bad := find_fault(nums)) is None:
            answer += 1
        elif find_fault(nums[:bad] + nums[bad + 1 :]) is None or find_fault(nums[: bad + 1] + nums[bad + 2 :]) is None:
            answer += 1
        elif bad == 1 and find_fault(nums[1:]) is None:
            # Edge case where removing the first number changes the calculated sign of the sequence.
            # Removing it (and causing the sign to change) could make the sequence valid.
            answer += 1
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
