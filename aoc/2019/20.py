from collections import defaultdict
from io import StringIO, TextIOBase
import sys

# The $ are there to prevent the editor from stripping trailing whitespace
part1_test_input = """                   A               $
                   A               $
  #################.#############  $
  #.#...#...................#.#.#  $
  #.#.#.###.###.###.#########.#.#  $
  #.#.#.......#...#.....#.#.#...#  $
  #.#########.###.#####.#.#.###.#  $
  #.............#.#.....#.......#  $
  ###.###########.###.#####.#.#.#  $
  #.....#        A   C    #.#.#.#  $
  #######        S   P    #####.#  $
  #.#...#                 #......VT$
  #.#.#.#                 #.#####  $
  #...#.#               YN....#.#  $
  #.###.#                 #####.#  $
DI....#.#                 #.....#  $
  #####.#                 #.###.#  $
ZZ......#               QG....#..AS$
  ###.###                 #######  $
JO..#.#.#                 #.....#  $
  #.#.#.#                 ###.#.#  $
  #...#..DI             BU....#..LF$
  #####.#                 #.#####  $
YN......#               VT..#....QG$
  #.###.#                 #.###.#  $
  #.#...#                 #.....#  $
  ###.###    J L     J    #.#.###  $
  #.....#    O F     P    #.#...#  $
  #.###.#####.#.#####.#####.###.#  $
  #...#.#.#...#.....#.....#.#...#  $
  #.#####.###.###.#.#.#########.#  $
  #...#.#.....#...#.#.#.#.....#.#  $
  #.###.#####.###.###.#.#.#######  $
  #.#.........#...#.............#  $
  #########.###.###.#############  $
           B   J   C               $
           U   P   P               $"""

part1_test_output = 58


def part1(inp: TextIOBase):
    answer = None

    map = [list(line.removesuffix("$")) for line in inp.readlines()]
    portal_labels = defaultdict(list)
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if "A" <= cell <= "Z":
                for dx, dy in [(0, 1), (1, 0)]:
                    new_x, new_y = x + dx, y + dy
                    if not (0 <= new_x < len(row) and 0 <= new_y < len(map)):
                        continue
                    cell2 = map[new_y][new_x]
                    if "A" <= cell2 <= "Z":
                        try:
                            t_x, t_y = new_x + dx, new_y + dy
                            assert (
                                map[t_y][t_x] == "."
                            ), f"{x=}, {y=} => {cell} {new_x=}, {new_y=} => {cell2}, {t_x=}, {t_y=}"
                        except (IndexError, AssertionError):
                            t_x, t_y = x - dx, y - dy
                            assert (
                                map[t_y][t_x] == "."
                            ), f"{x=}, {y=} => {cell} {new_x=}, {new_y=} => {cell2}, {t_x=}, {t_y=}"
                        if cell == cell2 == "A":
                            start = (t_x, t_y)
                            continue
                        if cell == cell2 == "Z":
                            end = (t_x, t_y)
                            continue
                        portal_labels[cell + cell2].append((t_x, t_y))
    print(portal_labels)
    print(start, end)

    portals = {p1: p2 for _, (p1, p2) in portal_labels.items()}
    portals.update({p2: p1 for _, (p1, p2) in portal_labels.items()})

    queue = [(start, 0)]
    visited = set()
    while queue:
        (x, y), steps = queue.pop(0)
        if (x, y) == end:
            answer = steps
            break
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if map[new_y][new_x] != ".":
                continue
            queue.append(((new_x, new_y), steps + 1))
        if (x, y) in portals:
            queue.append((portals[(x, y)], steps + 1))

    return answer


part2_test_input = """             Z L X W       C                 $
             Z P Q B       K                 $
  ###########.#.#.#.#######.###############  $
  #...#.......#.#.......#.#.......#.#.#...#  $
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  $
  #.#...#.#.#...#.#.#...#...#...#.#.......#  $
  #.###.#######.###.###.#.###.###.#.#######  $
  #...#.......#.#...#...#.............#...#  $
  #.#########.#######.#.#######.#######.###  $
  #...#.#    F       R I       Z    #.#.#.#  $
  #.###.#    D       E C       H    #.#.#.#  $
  #.#...#                           #...#.#  $
  #.###.#                           #.###.#  $
  #.#....OA                       WB..#.#..ZH$
  #.###.#                           #.#.#.#  $
CJ......#                           #.....#  $
  #######                           #######  $
  #.#....CK                         #......IC$
  #.###.#                           #.###.#  $
  #.....#                           #...#.#  $
  ###.###                           #.#.#.#  $
XF....#.#                         RF..#.#.#  $
  #####.#                           #######  $
  #......CJ                       NM..#...#  $
  ###.#.#                           #.###.#  $
RE....#.#                           #......RF$
  ###.###        X   X       L      #.#.#.#  $
  #.....#        F   Q       P      #.#.#.#  $
  ###.###########.###.#######.#########.###  $
  #.....#...#.....#.......#...#.....#.#...#  $
  #####.#.###.#######.#######.###.###.#.#.#  $
  #.......#.......#.#.#.#.#...#...#...#.#.#  $
  #####.###.#####.#.#.#.#.###.###.#.###.###  $
  #.......#.....#.#...#...............#...#  $
  #############.#.#.###.###################  $
               A O F   N                     $
               A A D   M                     $"""

part2_test_output = 396


def part2(inp: TextIOBase):
    map = [list(line.rstrip("\n$")) for line in inp.readlines()]
    portal_labels = defaultdict(list)
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if "A" <= cell <= "Z":
                for dx, dy in [(0, 1), (1, 0)]:
                    new_x, new_y = x + dx, y + dy
                    if not (0 <= new_x < len(row) and 0 <= new_y < len(map)):
                        continue
                    cell2 = map[new_y][new_x]
                    if "A" <= cell2 <= "Z":
                        try:
                            t_x, t_y = new_x + dx, new_y + dy
                            assert (
                                map[t_y][t_x] == "."
                            ), f"{x=}, {y=} => {cell} {new_x=}, {new_y=} => {cell2}, {t_x=}, {t_y=}"
                        except (IndexError, AssertionError):
                            t_x, t_y = x - dx, y - dy
                            assert (
                                map[t_y][t_x] == "."
                            ), f"{x=}, {y=} => {cell} {new_x=}, {new_y=} => {cell2}, {t_x=}, {t_y=}"
                        if cell == cell2 == "A":
                            start = (t_x, t_y)
                            continue
                        if cell == cell2 == "Z":
                            end = (t_x, t_y)
                            continue

                        inside = t_x != 2 and t_x != len(row) - 3 and t_y != 2 and t_y != len(map) - 3
                        if cell + cell2 == "LW":
                            print(cell, cell2, t_x, t_y, inside, len(row), len(map))
                        portal_labels[cell + cell2].append(((t_x, t_y), inside))
    print(portal_labels)
    print(start, end)

    portals = {p1: (p2, inside, label) for label, ((p1, inside), (p2, _)) in portal_labels.items()}
    portals.update({p2: (p1, not inside, label) for label, ((p1, inside), (p2, _)) in portal_labels.items()})

    print(portals)
    queue = [(start, 0, 0)]
    visited = set()
    answer = None
    while queue:
        (x, y), depth, steps = queue.pop(0)
        if (x, y) == end and depth == 0:
            answer = steps
            break
        if (x, y, depth) in visited:
            continue
        visited.add((x, y, depth))
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if map[new_y][new_x] != ".":
                continue
            queue.append(((new_x, new_y), depth, steps + 1))
        if (x, y) in portals:
            dest, inwards, label = portals[(x, y)]
            if not inwards:
                if depth == 0:
                    continue
                queue.append((dest, depth - 1, steps + 1))
            else:
                queue.append((dest, depth + 1, steps + 1))
            print(f"{label=} {(x, y)} -> {dest} ({depth=}, {inwards=})")

    return answer


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
