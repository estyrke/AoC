from collections import defaultdict
from functools import cmp_to_key
from io import StringIO, TextIOWrapper
import sys

part1_test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

part1_test_output = 143


def part1(inp: TextIOWrapper):
    answer = 0

    page_map: dict[str, set[str]] = defaultdict(set)
    page_map_rev: dict[str, set[str]] = defaultdict(set)
    map_lines, pages_lines = inp.read().split("\n\n")
    for line in map_lines.split("\n"):
        before, after = line.split("|")
        page_map[before.strip()].add(after.strip())
        page_map_rev[after.strip()].add(before.strip())

    for line in pages_lines.strip().split("\n"):
        pages = [p.strip() for p in line.split(",")]
        ok = True
        for i, page in enumerate(pages):
            for j, page2 in enumerate(pages[i + 1 :]):
                if page in page_map.get(page2, set()):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            answer += int(pages[len(pages) // 2])

    return answer


part2_test_input = part1_test_input

part2_test_output = 123


def part2(inp: TextIOWrapper):
    answer = 0

    page_map: dict[str, set[str]] = defaultdict(set)
    page_map_rev: dict[str, set[str]] = defaultdict(set)
    map_lines, pages_lines = inp.read().split("\n\n")
    for line in map_lines.split("\n"):
        before, after = line.split("|")
        page_map[before.strip()].add(after.strip())
        page_map_rev[after.strip()].add(before.strip())

    print(page_map)
    for line in pages_lines.strip().split("\n"):
        pages = [p.strip() for p in line.split(",")]

        new_pages = sorted(
            pages,
            key=cmp_to_key(lambda x, y: -1 if y in page_map.get(x, set()) else 1 if x in page_map.get(y, set()) else 0),
        )

        if new_pages == pages:
            continue
        answer += int(new_pages[len(new_pages) // 2])

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
