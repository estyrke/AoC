from io import StringIO, TextIOBase
import itertools
import operator
import sys

part1_test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

part1_test_output = 3749


def part1(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        total, nums = line.split(":")
        total = int(total)
        nums = [int(n) for n in nums.split()]
        print(total, nums)
        for ops in itertools.product([operator.add, operator.mul], repeat=(len(nums) - 1)):
            res = nums[0]
            for i, n in enumerate(nums[1:]):
                res = ops[i](res, n)
            if res == total:
                print(res, end=" ")
                print("FOUND")
                answer += res
                break
    return answer


part2_test_input = part1_test_input

part2_test_output = 11387


def concat(a: int, b: int):
    return int(str(a) + str(b))


def part2(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        total, nums = line.split(":")
        total = int(total)
        nums = [int(n) for n in nums.split()]
        print(total, nums)
        for ops in itertools.product([operator.add, operator.mul, concat], repeat=(len(nums) - 1)):
            res = nums[0]
            for i, n in enumerate(nums[1:]):
                res = ops[i](res, n)
            print(res, end=" ")
            if res == total:
                print("FOUND")
                answer += res
                break
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
