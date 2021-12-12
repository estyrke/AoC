# ## --- Part Two ---
#
# *Ding!* The "fasten seat belt" signs have turned on. Time to find your
# seat.
#
# It's a completely full flight, so your seat should be the only missing
# boarding pass in your list. However, there's a catch: some of the
# seats at the very front and back of the plane don't exist on this
# aircraft, so they'll be missing from your list as well.
#
# Your seat wasn't at the very front or back, though; the seats with IDs
# +1 and -1 from yours will be in your list.
#
# *What is the ID of your seat?*


def solve(inp):
    answer = None

    max = 0
    seats = []
    for line in inp.readlines():
        row = col = 0
        for p in line:
            if p == "F":
                row = row << 1 + 0
            elif p == "B":
                row = (row << 1) + 1
            elif p == "L":
                col = col << 1 + 0
            elif p == "R":
                col = (col << 1) + 1
        seat = row * 8 + col
        seats.append(seat)
        if seat > max:
            max = seat
    for i in range(max + 1):
        if not i in seats and i + 1 in seats and i - 1 in seats:
            answer = i
    return answer
