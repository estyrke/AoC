from io import TextIOWrapper
import math

###
# ## --- Part Two ---
# 
# Suddenly, the experimental antenna control console lights up:
# 
# 
# ```
# *Sleigh keys detected!*
# ```
# 
# According to the console, the keys are *directly under the submarine*.
# You landed right on them! Using a robotic arm on the submarine, you
# move the sleigh keys into the airlock.
# 
# Now, you just need to get them to Santa in time to save Christmas! You
# check your clock - it *is* Christmas. There's no way you can get them
# back to the surface in time.
# 
# Just as you start to lose hope, you notice a button on the sleigh
# keys: *remote start*. You can start the sleigh from the bottom of the
# ocean! You just need some way to *boost the signal* from the keys so
# it actually reaches the sleigh. Good thing the submarine has that
# experimental antenna! You'll definitely need *50 stars* to boost it
# that far, though.
# 
# The experimental antenna control console lights up again:
# 
# 
# ```
# *Energy source detected.
# Integrating energy source from device "sleigh keys"...done.
# Installing device drivers...done.
# Recalibrating experimental antenna...done.
# Boost strength due to matching signal phase: *1 star**
# ```
# 
# Only *49 stars* to go.
###

test_input = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

test_output = 58


def solve(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    state = [list(l.strip()) for l in inp.readlines()]

    i = 0
    rows = len(state)
    cols = len(state[0])
    while True:
        i += 1
        print(i)
        # print(state)
        state1 = move_east(state, rows, cols)
        state2 = move_south(state1, rows, cols)
        if state2 == state:
            return i
        state = state2
        # if i > 5:
        #    break


def move_east(state, rows, cols):
    new_state = []
    for y, line in enumerate(state):
        new_line = ["."] * cols
        for x, c in enumerate(line):
            if c == ">":
                if state[y][(x + 1) % cols] == ".":
                    new_line[(x + 1) % cols] = ">"
                else:
                    new_line[x] = ">"
            elif c == "v":
                new_line[x] = c
        new_state.append(new_line)
    return new_state


def move_south(state, rows, cols):
    new_state = [["."] * cols for _ in range(rows)]
    print(len(new_state[0]))
    for y, line in enumerate(state):
        for x, c in enumerate(line):
            if c == "v":
                if state[(y + 1) % rows][x] == ".":
                    new_state[y][x] = "."
                    new_state[(y + 1) % rows][x] = "v"
                else:
                    new_state[y][x] = "v"
            elif c == ">":
                new_state[y][x] = ">"
            else:
                assert c == "."
    return new_state
