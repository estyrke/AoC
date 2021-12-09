from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# Impressed, the Elves issue you a challenge: determine the `30000000`th
# number spoken. For example, given the same starting numbers as above:
#
# * Given `0,3,6`, the `30000000`th number spoken is `175594`.
# * Given `1,3,2`, the `30000000`th number spoken is `2578`.
# * Given `2,1,3`, the `30000000`th number spoken is `3544142`.
# * Given `1,2,3`, the `30000000`th number spoken is `261214`.
# * Given `2,3,1`, the `30000000`th number spoken is `6895259`.
# * Given `3,2,1`, the `30000000`th number spoken is `18`.
# * Given `3,1,2`, the `30000000`th number spoken is `362`.
#
#
# Given your starting numbers, *what will be the `30000000`th number
# spoken?*
###


def solve(inp):
    inp = inp.readline()
    # inp = "3,1,2"
    spoken = [int(i) for i in inp.strip().split(",")]
    ages = {num: -i for i, num in enumerate(spoken[:-1])}
    last_spoken = spoken[-1]
    for i in range(len(spoken) - 1, 30000000 - 1):
        if last_spoken not in ages:
            ages[last_spoken] = -i
            last_spoken = 0
        else:
            prev_age, ages[last_spoken] = ages[last_spoken], -i
            last_spoken = i + prev_age
    return last_spoken
