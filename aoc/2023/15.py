from io import StringIO, TextIOWrapper
import sys

part1_test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

part1_test_output = 1320


def HASH(s: str) -> int:
    res = 0
    for c in s:
        res = ((res + ord(c)) * 17) % 256
    return res


def part1(inp: TextIOWrapper):
    answer = 0

    tokens = inp.readline().strip().split(",")
    for t in tokens:
        answer += HASH(t)

    return answer


part2_test_input = part1_test_input

part2_test_output = 145


def part2(inp: TextIOWrapper):
    answer = None

    tokens = inp.readline().strip().split(",")

    boxes = [dict() for _ in range(256)]

    for t in tokens:
        label = t.rstrip("-=0123456789")
        box = HASH(label)
        if "=" in t:
            label, focus = t.split("=")
            boxes[box][label] = int(focus)
        else:
            assert "-" in t
            boxes[box].pop(t[:-1], None)

    answer = 0
    for i, b in enumerate(boxes):
        for sn, (l, f) in enumerate(b.items()):
            fp = (1 + i) * (sn + 1) * f
            answer += fp

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
