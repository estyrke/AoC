from io import TextIOWrapper
import math
from typing import List
import itertools

###
# ## --- Part Two ---
#
# You notice a second question on the back of the homework assignment:
#
# What is the largest magnitude you can get from adding only two of the
# snailfish numbers?
#
# Note that snailfish addition is not
# [commutative](https://en.wikipedia.org/wiki/Commutative_property) -
# that is, `x + y` and `y + x` can produce different results.
#
# Again considering the last example homework assignment above:
#
#
# ```
# [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
# [[[5,[2,8]],4],[5,[[9,9],0]]]
# [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
# [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
# [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
# [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
# [[[[5,4],[7,7]],8],[[8,3],8]]
# [[9,3],[[9,9],[6,[4,9]]]]
# [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
# [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
#
# ```
#
# The largest magnitude of the sum of any two snailfish numbers in this
# list is `*3993*`. This is the magnitude of
# `[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]` +
# `[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]`, which reduces to
# `[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]`.
#
# *What is the largest magnitude of any sum of two different snailfish
# numbers from the homework assignment?*
###

test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

test_output = 3993


def solve(inp: TextIOWrapper):
    nums = [list(line.strip()) for line in inp.readlines()]
    nums = [[int(n) if n.isnumeric() else n for n in num if n != ","] for num in nums]

    max_mag = 0
    for n1, n2 in itertools.permutations(nums, 2):
        res = magnitude_literal(add(n1, n2))
        if res > max_mag:
            max_mag = res
    return max_mag


def magnitude_literal(num) -> int:
    py_str = ""
    for i, token in enumerate(num):
        if (
            i < len(num) - 1
            and isinstance(num[i], int)
            and (num[i + 1] == "[" or isinstance(num[i + 1], int))
        ):
            py_str += f"{token}, "
        elif (
            i < len(num) - 1
            and num[i] == "]"
            and (num[i + 1] == "[" or isinstance(num[i + 1], int))
        ):
            py_str += f"{token}, "
        else:
            py_str += str(token)
    return magnitude(eval(py_str))


def magnitude(num) -> int:
    if isinstance(num, int):
        return num
    else:
        assert len(num) == 2
        return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


def add(num1, num2):
    num = ["["] + num1 + num2 + ["]"]

    return reduce(num)


def reduce(num):
    while True:
        if not explode(num) and not split(num):
            break

    return num


def explode(num: List):
    depth = 0
    next_parse_pos = 0
    for i, token in enumerate(num):
        if i < next_parse_pos:
            continue
        if isinstance(token, int):
            continue
        elif token == "[":
            if isinstance(num[i + 1], int) and isinstance(num[i + 2], int):
                assert num[i + 3] == "]"
                next_parse_pos = i + 4
                # pair
                if depth >= 4:
                    for j in range(i - 1, -1, -1):
                        if isinstance(num[j], int):
                            num[j] += num[i + 1]
                            break
                    for j in range(i + 3, len(num)):
                        if isinstance(num[j], int):
                            num[j] += num[i + 2]
                            break
                    num[i : i + 4] = [0]
                    return True
            else:
                depth += 1
        elif token == "]":
            depth -= 1
        else:
            assert token == ","
    return False


def split(num):
    for i, n in enumerate(num):
        if isinstance(n, int) and n >= 10:
            num[i : i + 1] = ["[", n // 2, math.ceil(n / 2.0), "]"]
            return True
    return False
