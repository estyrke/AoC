from functools import cache
from sympy.ntheory.factor_ import factorint
from io import StringIO, TextIOBase
import sys
import itertools

part1_test_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

part1_test_output = 1227775554


def part1(inp: TextIOBase):
    answer = 0

    ranges = inp.read().strip().split(",")
    ranges = [i.split("-") for i in ranges]
    ranges = [(int(i[0]), int(i[1])) for i in ranges]

    for start, end in ranges:
        for id in range(start, end + 1):
            sid = str(id)
            if len(sid) % 2 != 0:
                continue
            if sid[: len(sid) // 2] == sid[len(sid) // 2 :]:
                answer += id

    return answer


part2_test_input = part1_test_input

part2_test_output = 4174379265


@cache
def factors(n: int):
    """Get all the ways to divide a number, including 1 but excluding the number itself."""
    factors = [1]
    for f, mult in factorint(n).items():
        print(f, mult)
        for i in range(1, mult + 1):
            if f**i == n:
                continue
            factors.append(f**i)
    return factors


def part2(inp: TextIOBase):
    answer = 0

    ranges = inp.read().strip().split(",")
    ranges = [i.split("-") for i in ranges]
    ranges = [(int(i[0]), int(i[1])) for i in ranges]

    for start, end in ranges:
        for id in range(start, end + 1):
            sid = str(id)
            # print(sid, prime_factors(len(sid)))
            for fact in factors(len(sid)):
                if fact == len(sid):
                    continue
                match = None
                for chunk in itertools.batched(sid, fact):
                    if match is None:
                        match = chunk
                    elif match != chunk:
                        break
                else:
                    print("Match", factors(len(sid)), fact, sid, "".join(match))
                    answer += id
                    break

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
