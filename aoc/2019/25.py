from io import StringIO, TextIOBase
from itertools import chain, combinations
import sys
from .intcode import Machine

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOBase):
    answer = None

    m = Machine.from_stream(inp)

    out = m.run([])
    assert out is not None
    print("".join(chr(c) if c < 256 else str(c) for c in out))

    for line in [
        "east",  # Sick bay
        "take whirled peas",
        "east",
        "north",  # Hallway
        "take prime number",
        "south",
        "east",
        "east",
        "east",  # Kitchen
        "take dark matter",
        "west",
        "west",
        "west",
        "west",
        "north",  # Passage
        "take coin",
        "west",
        "south",  # Storage
        "take antenna",
        "north",
        "north",  # Crew Quarters
        "west",
        "take astrolabe",
        "east",
        "south",
        "east",
        "south",
        "west",
        "north",  # Holodeck
        "take fixed point",
        "north",  # Navigation
        "take weather machine",
        "east",
        "south",
    ]:
        print(send_command(m, line))

    inventory = [
        "dark matter",
        "coin",
        "whirled peas",
        "fixed point",
        "astrolabe",
        "prime number",
        "antenna",
        "weather machine",
    ]

    # Brute force the combination of items to carry
    for item in inventory:
        send_command(m, f"drop {item}")

    for items in powerset(inventory):
        for item in items:
            send_command(m, f"take {item}")
        res = send_command(m, "south")
        if "lighter" not in res and "heavier" not in res:
            break
        for item in items:
            send_command(m, f"drop {item}")

    while True:
        line = input()
        print(send_command(m, line))
        if m.halted:
            break
    return answer


def send_command(m: Machine, line: str) -> str:
    out = m.run([ord(x) for x in line + "\n"])
    assert out is not None
    response = "".join(chr(c) if c < 256 else str(c) for c in out)
    return response


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOBase):
    answer = None

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
