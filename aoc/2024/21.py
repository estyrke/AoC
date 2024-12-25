from collections import defaultdict
from functools import cache
from io import StringIO, TextIOBase
from itertools import product
import sys


part1_test_input = """029A
980A
179A
456A
379A"""

part1_test_output = 126384

numeric_neighbors = {
    "A": [("0", "<"), ("3", "^")],
    "0": [("A", ">"), ("2", "^")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("1", "<"), ("5", "^"), ("0", "v"), ("3", ">")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("7", "^"), ("5", ">")],
    "5": [("2", "v"), ("8", "^"), ("4", "<"), ("6", ">")],
    "6": [("3", "v"), ("9", "^"), ("5", "<")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("9", ">"), ("7", "<")],
    "9": [("6", "v"), ("8", "<")],
}

directional_neighbors = {
    "A": {"^": ["<"], ">": ["v"], "v": ["<v", "v<"], "<": ["v<<"]},  # , "<v<"]},
    "^": {"A": [">"], "v": ["v"], "<": ["v<"], ">": ["v>", ">v"]},
    "v": {"<": ["<"], ">": [">"], "^": ["^"], "A": ["^>"]},  # , ">^"]},
    "<": {"v": [">"], "^": [">^"], ">": [">>"], "A": [">>^"]},  # , ">^>"]},
    ">": {"v": ["<"], "A": ["^"], "^": ["<^", "^<"], "<": ["<<"]},
}


def numeric_bfs(start, end):
    queue = [(start, "", "")]
    # visited = {start}
    min_sequence = None
    while queue:
        pos, path, sequence = queue.pop(0)
        if pos == end:
            min_sequence = len(sequence) if min_sequence is None else min(min_sequence, len(sequence))
            if min_sequence == len(sequence):
                yield sequence
        for neighbor, direction in numeric_neighbors[pos]:
            if neighbor not in path:
                # visited.add(neighbor)
                queue.append((neighbor, path + neighbor, sequence + direction))


def numeric_sequences(code: str):
    pos = "A"
    sequences = []
    for c in code:
        if c != pos:
            sequences.append(list(numeric_bfs(pos, c)))
        sequences.append(["A"])
        pos = c

    return ["".join(p) for p in product(*sequences)]


@cache
def directional_sequences2(code: str):
    pos = "A"
    sequences = []
    for c in code:
        if c != pos:
            sequences.append(directional_neighbors[pos][c][0] + "A")
        else:
            sequences.append("A")
        # sequences.append(["A"])
        pos = c
    return [s for s in sequences]


def part1(inp: TextIOBase):
    answer = 0

    codes: list[str] = [l.strip() for l in inp.readlines()]

    answer = 0
    for code in codes:
        print("code", code)
        numeric = int(code[:-1])
        length = run_robots2(code, 3)
        print(f"{code=}, {numeric=}, {length=}")
        assert length is not None
        answer += numeric * length
        # return None

    return answer


def run_robots2(code: str, steps: int):
    first_robot_seqs = numeric_sequences(code)
    # print("first_robot_seqs", first_robot_seqs)
    min_length = None
    for seq in first_robot_seqs:
        seq_parts = [s + "A" for s in seq.split("A")]
        counts = {k: seq_parts.count(k) for k in seq_parts}
        # print("seq_parts", seq_parts, counts)
        for step in range(steps):
            new_counts = defaultdict(int)
            for part, count in counts.items():
                sub_parts = directional_sequences2(part)
                # print("sub_parts", sub_parts)
                for sub_part in sub_parts:
                    new_counts[sub_part] += count
            # print(f"{step=} new_counts", new_counts)
            counts = dict(new_counts)
        length = sum([len(k) * v for k, v in counts.items()]) - 1
        min_length = length if min_length is None else min(min_length, length)
        # print("counts", counts, length, min_length)
    return min_length


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = 0
    codes: list[str] = [l.strip() for l in inp.readlines()]

    for code in codes:
        numeric = int(code[:-1])
        print("code", code)
        numeric = int(code[:-1])
        length = run_robots2(code, 25)
        assert length is not None
        print(f"{code=}, {numeric=}, {length=}")
        answer += numeric * length

    assert answer < 193369129748870
    assert answer > 77249080598684
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
