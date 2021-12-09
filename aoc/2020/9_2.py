from io import TextIOWrapper
import math
from typing import TextIO

###
# ## --- Part Two ---
#
# The final step in breaking the XMAS encryption relies on the invalid
# number you just found: you must *find a contiguous set of at least two
# numbers* in your list which sum to the invalid number from step 1.
#
# Again consider the above example:
#
#
# ```
# 35
# 20
# *15*
# *25*
# *47*
# *40*
# 62
# 55
# 65
# 95
# 102
# 117
# 150
# 182
# 127
# 219
# 299
# 277
# 309
# 576
#
# ```
#
# In this list, adding up all of the numbers from `15` through `40`
# produces the invalid number from step 1, `127`. (Of course, the
# contiguous set of numbers in your actual list might be much longer.)
#
# To find the *encryption weakness*, add together the *smallest* and
# *largest* number in this contiguous range; in this example, these are
# `15` and `47`, producing *`62`*.
#
# *What is the encryption weakness in your XMAS-encrypted list of
# numbers?*
###


def check_number(next, history):
    for i in history:
        if next - i in history and (next - i != i or history.count(i) > 1):
            return True
    return False


def check_contiguous(number, min_i, numbers):
    sum_cont = 0
    for max_i in range(min_i, len(numbers)):
        sum_cont += numbers[max_i]
        if max_i > min_i and sum_cont == number:
            return min(numbers[min_i : max_i + 1]) + max(numbers[min_i : max_i + 1])
        elif sum_cont > number:
            return None


def solve(inp: TextIOWrapper):
    numbers = [int(line) for line in inp.readlines()]
    history = []
    invalid = None
    for next_number in numbers:
        if len(history) > 25:
            history.pop(0)
        if len(history) == 25 and not check_number(next_number, history):
            invalid = next_number
            break

        history.append(next_number)

    print(invalid)
    for i in range(len(numbers)):
        weakness = check_contiguous(invalid, i, numbers)
        if weakness is not None:
            return weakness
