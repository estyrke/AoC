from io import TextIOWrapper
import math
from typing import List, Tuple

###
# # ## --- Day 18: Operation Order ---
#
# As you look out the window and notice a heavily-forested continent
# slowly appear over the horizon, you are interrupted by the child
# sitting next to you. They're curious if you could help them with their
# math homework.
#
# Unfortunately, it seems like this "math" [follows different
# rules](https://www.youtube.com/watch?v=3QtRK7Y2pPU&t=15) than you
# remember.
#
# The homework (your puzzle input) consists of a series of expressions
# that consist of addition (`+`), multiplication (`*`), and parentheses
# (`(...)`). Just like normal math, parentheses indicate that the
# expression inside must be evaluated before it can be used by the
# surrounding expression. Addition still finds the sum of the numbers on
# both sides of the operator, and multiplication still finds the
# product.
#
# However, the rules of *operator precedence* have changed. Rather than
# evaluating multiplication before addition, the operators have the
# *same precedence*, and are evaluated left-to-right regardless of the
# order in which they appear.
#
# For example, the steps to evaluate the expression `1 + 2 * 3 + 4 * 5 +
# 6` are as follows:
#
#
# ```
# *1 + 2* * 3 + 4 * 5 + 6
#   *3 * 3* + 4 * 5 + 6
#       *9 + 4* * 5 + 6
#          *13 * 5* + 6
#              *65 + 6*
#                  *71*
#
# ```
#
# Parentheses can override this order; for example, here is what happens
# if parentheses are added to form `1 + (2 * 3) + (4 * (5 + 6))`:
#
#
# ```
# 1 + *(2 * 3)* + (4 * (5 + 6))
# *1 + 6*    + (4 * (5 + 6))
#      7      + (4 * *(5 + 6)*)
#      7      + *(4 * 11 )*
#      *7 + 44*
#             *51*
#
# ```
#
# Here are a few more examples:
#
# * `2 * 3 + (4 * 5)` becomes *`26`*.
# * `5 + (8 * 3 + 9 + 3 * 4 * 3)` becomes *`437`*.
# * `5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))` becomes *`12240`*.
# * `((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2` becomes *`13632`*.
#
#
# Before you can help with the homework, you need to understand it
# yourself. *Evaluate the expression on each line of the homework; what
# is the sum of the resulting values?*
###

test_input = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

test_output = 26 + 437 + 12240 + 13632


def evaluate(expr: List) -> Tuple[int, List]:
    if len(expr) == 1:
        assert isinstance(expr[0], int)
        return expr[0], []
    if expr[0] == "(":
        lhs, expr = evaluate(expr[1:])
    else:
        lhs = expr.pop(0)

    op = expr.pop(0)
    if op == ")":
        return lhs, expr

    if expr[0] == "(":
        rhs, expr = evaluate(expr[1:])
    else:
        rhs = expr.pop(0)

    if op == "+":
        answer = evaluate([lhs + rhs] + expr)
    else:
        assert op == "*"
        answer = evaluate([lhs * rhs] + expr)
    return answer


def solve(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        tokens = line.replace("(", "( ").replace(")", " )").split()
        tokens = [int(token) if token.isdigit() else token for token in tokens]
        answer += evaluate(tokens)[0]
    return answer
