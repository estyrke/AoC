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


@lru_cache
def split(record: str, groups: tuple[int], current_group=0) -> int:
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
        return split("." + record[1:], groups, current_group) + split(
            "#" + record[1:], groups, current_group
        )
    return 0


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        record, groups = line.strip().split()
        groups = tuple([int(g) for g in groups.split(",")])

        answer += split(record, groups)

    return answer


part2_test_input = part1_test_input

part2_test_output = 525152


def part2(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        record, groups = line.strip().split()
        record = "?".join([record, record, record, record, record])
        groups = tuple(int(g) for g in groups.split(","))
        groups = (*groups, *groups, *groups, *groups, *groups)

        answer += split(record, groups)
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
