from io import StringIO, TextIOBase
import sys

part1_test_input = """2333133121414131402"""

part1_test_output = 1928


def back_blocks(table):
    for i in range(len(table) - 1, -1, -2):
        for _ in range(table[i]):
            yield i // 2


def part1(inp: TextIOBase):
    answer = 0

    table = [int(x) for x in inp.read().strip()]
    files = table[::2]
    total_blocks = sum(files)

    front = 0
    back = len(table) - 1
    assert back % 2 == 0
    is_front = True
    block = 0
    sub_block = 0
    hole_len = 0
    back_gen = back_blocks(table)
    while block < total_blocks:
        sub_block += 1

        if is_front:
            file_id = front // 2
            answer += block * file_id
            if sub_block >= table[front]:
                hole_len = table[front + 1]
                front += 2
                sub_block = 0
                is_front = False
            block += 1
        else:
            for _ in range(hole_len):
                file_id = next(back_gen)
                answer += file_id * block
                block += 1
                if block >= total_blocks:
                    break
            is_front = True
            sub_block = 0
    return answer


part2_test_input = part1_test_input

part2_test_output = 2858


def part2(inp: TextIOBase):
    table = [int(x) for x in inp.read().strip()]
    files: list[tuple[int, int, int]] = []
    holes: list[tuple[int, int]] = []
    pos = 0
    for i in range(0, len(table), 2):
        if i > 0:
            pos += table[i - 1]
        files.append((pos, table[i], i // 2))
        pos += table[i]

    pos = 0
    for i in range(1, len(table), 2):
        pos += table[i - 1]
        holes.append((pos, table[i]))
        pos += table[i]

    for pos, size, file_id in reversed(files):
        for i, (hole_pos, hole_size) in enumerate(holes):
            if pos > hole_pos and size <= hole_size:
                holes[i] = (hole_pos + size, hole_size - size)
                for j, (hole_pos2, hole_size2) in enumerate(holes):
                    if hole_pos2 < pos and (j + 1 >= len(holes) or holes[j + 1][0] > pos):
                        if j + 1 < len(holes):
                            next_hole_size = holes[j + 1][1]
                            del holes[j + 1]
                        else:
                            next_hole_size = 0
                        holes[j] = (hole_pos2, hole_size2 + size + next_hole_size)
                        break
                files[file_id] = (hole_pos, size, file_id)
                break

    packed = sorted(files)
    answer = 0
    for pos, size, file_id in packed:
        for i in range(size):
            answer += (pos + i) * file_id
    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
