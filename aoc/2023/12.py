from functools import lru_cache
from io import StringIO, TextIOWrapper
import sys

part1_test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

part1_test_output = 21


def split(record: list[str], groups: list[int], current_group=0) -> int:
    if len(record) == 0:
        if len(groups) == 0 or (len(groups) == 1 and current_group == groups[0]):
            return 1
        return 0
    if record[0] == ".":
        if len(groups) == 0 and current_group > 0:
            return 0
        if len(groups) > 0 and current_group > groups[0]:
            return 0
        if current_group == 0:
            return split(record[1:], groups, 0)
        if len(groups) == 0:
            return 0
        if groups[0] != current_group:
            return 0
        return split(record[1:], groups[1:], 0)
    if record[0] == "#":
        if len(groups) == 0:
            return 0
        if current_group + 1 > groups[0]:
            return 0
        return split(record[1:], groups, current_group + 1)
    if record[0] == "?":
        return split([".", *record[1:]], groups, current_group) + split(
            ["#", *record[1:]], groups, current_group
        )
    return 0


@lru_cache
def split2(record: str, groups: tuple[int]) -> int:
    if len(groups) == 0:
        if all([c in ["?", "."] for c in record]):
            return 1
        return 0

    gl = groups[0]
    res = 0
    # print(f"{record} {groups}:")
    for i in range(len(record) - gl + 1):
        if all(c in "?." for c in record[0:i]) and all(
            c in "?#" for c in record[i : i + gl]
        ):
            if i + gl == len(record):
                if len(groups) == 1:
                    # print(f"  Matched {gl} at {i} (final)")
                    res += 1
            elif record[i + gl] in "?.":
                # print(f"  Matched {gl} at {i}")
                res += split2(record[i + gl + 1 :], groups[1:])
    return res


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        record, groups = line.strip().split()
        record = list(record)
        groups = [int(g) for g in groups.split(",")]

        split2.cache_clear()
        answer += (s := split(record, groups))
        # print(s)

    return answer


part2_test_input = part1_test_input

part2_test_output = 525152


def part2(inp: TextIOWrapper):
    answer = 0

    for i, line in enumerate(inp.readlines()):
        record, groups = line.strip().split()
        record = "?".join([record, record, record, record, record])
        groups = tuple(int(g) for g in groups.split(","))
        groups = (*groups, *groups, *groups, *groups, *groups)

        answer += (s := split2(record, groups))
        print(i + 1, s)
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
