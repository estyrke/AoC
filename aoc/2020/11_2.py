from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# As soon as people start to arrive, you realize your mistake. People
# don't just care about adjacent seats - they care about *the first seat
# they can see* in each of those eight directions!
#
# Now, instead of considering just the eight immediately adjacent seats,
# consider the *first seat* in each of those eight directions. For
# example, the empty seat below would see *eight* occupied seats:
#
#
# ```
# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
#
# ```
#
# The leftmost empty seat below would only see *one* empty seat, but
# cannot see any of the occupied ones:
#
#
# ```
# .............
# .L.L.#.#.#.#.
# .............
#
# ```
#
# The empty seat below would see *no* occupied seats:
#
#
# ```
# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
#
# ```
#
# Also, people seem to be more tolerant than you expected: it now takes
# *five or more* visible occupied seats for an occupied seat to become
# empty (rather than *four or more* from the previous rules). The other
# rules still apply: empty seats that see no occupied seats become
# occupied, seats matching no rule don't change, and floor never
# changes.
#
# Given the same starting layout as above, these new rules cause the
# seating area to shift around as follows:
#
#
# ```
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
#
# ```
#
#
# ```
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
#
# ```
#
#
# ```
# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#
#
# ```
#
#
# ```
# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#
#
# ```
#
#
# ```
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#
#
# ```
#
#
# ```
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
#
# ```
#
#
# ```
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
#
# ```
#
# Again, at this point, people stop shifting around and the seating area
# reaches equilibrium. Once this occurs, you count *`26`* occupied
# seats.
#
# Given the new visibility method and the rule change for occupied seats
# becoming empty, once equilibrium is reached, *how many seats end up
# occupied?*
###


def calc_occupied(seats, row, col):
    occ = 0
    max_row = len(seats) - 1
    max_col = len(seats[0]) - 1
    for row_d in [-1, 0, 1]:
        for col_d in [-1, 0, 1]:
            if row_d == col_d == 0:
                continue
            test_row = row
            test_col = col

            while True:
                test_row, test_col = test_row + row_d, test_col + col_d
                if (
                    test_row < 0
                    or test_col < 0
                    or test_row > max_row
                    or test_col > max_col
                ):
                    break
                if seats[test_row][test_col] == "#":
                    occ += 1
                    break
                elif seats[test_row][test_col] == "L":
                    break
    return occ


def solve(inp: TextIOWrapper):
    answer = None
    seats = []
    for line in inp.readlines():
        seats.append(list(line.strip()))

    changed = True
    while changed:
        changed = False
        new_seats = [[s for s in row] for row in seats]
        for row in range(len(seats)):
            for col in range(len(seats[0])):
                # * If a seat is *empty* (`L`) and there are *no* occupied seats
                # adjacent to it, the seat becomes *occupied*.
                # * If a seat is *occupied* (`#`) and *four or more* seats adjacent to
                # it are also occupied, the seat becomes *empty*.
                # * Otherwise, the seat's state does not change.
                occupied = calc_occupied(seats, row, col)
                if seats[row][col] == "L" and occupied == 0:
                    new_seats[row][col] = "#"
                    changed = True
                elif seats[row][col] == "#" and occupied >= 5:
                    new_seats[row][col] = "L"
                    changed = True
        seats = new_seats

    # print(seats)
    answer = sum([row.count("#") for row in seats])
    return answer
