from io import StringIO, TextIOBase
import sys

part1_test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

part1_test_output = 22

IS_TEST: bool = False


def bfs(map, pos, target):
    q = [(pos, [pos])]
    seen = set()
    while q:
        (x, y), path = q.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if (x, y) == target:
            return len(path) - 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or nx >= len(map[0]) or ny >= len(map):
                continue
            if map[ny][nx] == "#":
                continue
            q.append(((nx, ny), path + [(nx, ny)]))
    return None


def part1(inp: TextIOBase):
    if IS_TEST:
        w, h = 7, 7
        steps = 12
    else:
        w, h = 71, 71
        steps = 1024

    bytes = [tuple(int(b) for b in l.split(",")) for l in inp.readlines()]

    map = [["." for _ in range(w)] for _ in range(h)]
    for i in range(steps):
        x, y = bytes[i]
        map[y][x] = "#"

    return bfs(map, (0, 0), (w - 1, h - 1))


part2_test_input = part1_test_input

part2_test_output = "6,1"


def part2(inp: TextIOBase):
    if IS_TEST:
        w, h = 7, 7
    else:
        w, h = 71, 71

    bytes = [tuple(int(b) for b in l.split(",")) for l in inp.readlines()]

    max_steps = len(bytes)
    min_steps = 0
    while True:
        curr_steps = (max_steps + min_steps) // 2
        print(min_steps, max_steps, curr_steps)
        map = [["." for _ in range(w)] for _ in range(h)]
        for i in range(curr_steps):
            x, y = bytes[i]
            map[y][x] = "#"
        res = bfs(map, (0, 0), (w - 1, h - 1))
        if res is None:
            max_steps = curr_steps
        else:
            min_steps = curr_steps
        if max_steps - min_steps <= 1:
            return ",".join(str(b) for b in bytes[max_steps - 1])


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
