from io import TextIOWrapper
import math
from itertools import count
from typing import List, Optional, Tuple

"""
## --- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the
Venus refuelling station. During the rush back on Earth, the fuel
management system wasn't completely installed, so that's next on the
priority list.

Opening the front panel reveals a jumble of wires. Specifically, *two
wires* are connected to a central port and extend outward on a grid.
You trace the path each wire takes as it leaves the central port, one
wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths.
To fix the circuit, you need to *find the intersection point closest
to the central port*. Because the wires are on a grid, use the
[Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry)
for this measurement. While the wires do technically cross right at
the central port where they both start, this point does not count, nor
does a wire count as crossing with itself.

For example, if the first wire's path is `R8,U5,L5,D3`, then starting
from the central port (`o`), it goes right `8`, up `5`, left `5`, and
finally down `3`:


```
...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

```

Then, if the second wire's path is `U7,R6,D4,L4`, it goes up `7`,
right `6`, down `4`, and left `4`:


```
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-*X*--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

```

These wires cross at two locations (marked `X`), but the lower-left
one is closer to the central port: its distance is `3 + 3 = 6`.

Here are a few more examples:

* `R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83` = distance `159`
* `R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7` = distance `135`


*What is the Manhattan distance* from the central port to the closest
intersection?
"""

part1_test_input = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"""
part1_test_input = """R8,U5,L5,D3
U7,R6,D4,L4"""
part1_test_output = 159
part1_test_output = 6


def is_vertical(p1, p2) -> bool:
    is_vertical = p1[0] == p2[0]
    is_horizontal = p1[1] == p2[1]
    assert is_vertical != is_horizontal
    return is_vertical


def crossing_distance(p11, p12, p21, p22) -> Optional[int]:
    if is_vertical(p11, p12) == is_vertical(p21, p22):
        return None

    if is_vertical(p11, p12):
        x_cross = p11[0]
        y_cross = p21[1]
        if p21[0] < x_cross < p22[0] and p11[1] < y_cross < p12[1]:
            return abs(x_cross) + abs(y_cross)
    else:
        assert is_vertical(p21, p22)
        x_cross = p21[0]
        y_cross = p11[1]
        if p11[0] < x_cross < p12[0] and p21[1] < y_cross < p22[1]:
            return abs(x_cross) + abs(y_cross)

    return None


def part1(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    wires = [l.strip().split(",") for l in inp.readlines()]

    wire_pos: List[List[Tuple[int, int]]] = [[(0, 0)] for _ in range(len(wires))]

    for w in range(len(wires)):
        for move in wires[w]:
            last_pos = wire_pos[w][-1]
            if move.startswith("R"):
                wire_pos[w].append((last_pos[0] - int(move[1:]), last_pos[1]))
            elif move.startswith("L"):
                wire_pos[w].append((last_pos[0] + int(move[1:]), last_pos[1]))
            elif move.startswith("U"):
                wire_pos[w].append((last_pos[0], last_pos[1] - int(move[1:])))
            else:
                assert move.startswith("D")
                wire_pos[w].append((last_pos[0], last_pos[1] + int(move[1:])))

    crossings = []
    for i1 in range(1, len(wire_pos[0])):
        for i2 in range(1, len(wire_pos[1])):
            c = crossing_distance(
                wire_pos[0][i1 - 1],
                wire_pos[0][i1],
                wire_pos[1][i2 - 1],
                wire_pos[1][i2],
            )
            if c is not None:
                crossings.append(c)

    return min(crossings)


"""
## --- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually
need to *minimize the signal delay*.

To do this, calculate the *number of steps* each wire takes to reach
each intersection; choose the intersection where the *sum of both
wires' steps* is lowest. If a wire visits a position on the grid
multiple times, use the steps value from the *first* time it visits
that position when calculating the total value of a specific
intersection.

The number of steps a wire takes is the total number of grid squares
the wire has entered to get to that location, including the
intersection being considered. Again consider the example from above:


```
...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

```

In the above example, the intersection closest to the central port is
reached after `8+5+5+2 = *20*` steps by the first wire and `7+6+4+3 =
*20*` steps by the second wire for a total of `20+20 = *40*` steps.

However, the top-right intersection is better: the first wire takes
only `8+5+2 = *15*` and the second wire takes only `7+6+2 = *15*`, a
total of `15+15 = *30*` steps.

Here are the best steps for the extra examples from above:

* `R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83` = `610` steps
* `R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7` = `410` steps


*What is the fewest combined steps the wires must take to reach an
intersection?*
"""

part2_test_input = part1_test_input

part2_test_output = 30


def part2(inp: TextIOWrapper):
    wires = [l.strip().split(",") for l in inp.readlines()]

    wire_trace = [{}, {}]
    crossings = []
    for w in range(len(wires)):
        pos = (0, 0)
        total = 0
        for move in wires[w]:
            if move.startswith("R"):
                delta = (1, 0)
            elif move.startswith("L"):
                delta = (-1, 0)
            elif move.startswith("U"):
                delta = (0, -1)
            else:
                assert move.startswith("D")
                delta = (0, 1)
            dist = int(move[1:])
            for i in range(dist):
                pos = tuple(p + d for p, d in zip(pos, delta))
                total += 1
                wire_trace[w][pos] = total

                if w > 0 and pos in wire_trace[0]:
                    crossings.append(total + wire_trace[0][pos])

    answer = min(crossings)
    return answer
