from io import TextIOWrapper
import math
from typing import List, Tuple

###
# ## --- Part Two ---
#
# You manage to answer the child's questions and they finish part 1 of
# their homework, but get stuck when they reach the next section:
# *advanced* math.
#
# Now, addition and multiplication have *different* precedence levels,
# but they're not the ones you're familiar with. Instead, addition is
# evaluated *before* multiplication.
#
# For example, the steps to evaluate the expression `1 + 2 * 3 + 4 * 5 +
# 6` are now as follows:
#
#
# ```
# *1 + 2* * 3 + 4 * 5 + 6
#   3   * *3 + 4* * 5 + 6
#   3   *   7   * *5 + 6*
#   *3 * 7*   *  11
#      *21 * 11*
#          *231*
#
# ```
#
# Here are the other examples from above:
#
# * `1 + (2 * 3) + (4 * (5 + 6))` still becomes *`51`*.
# * `2 * 3 + (4 * 5)` becomes *`46`*.
# * `5 + (8 * 3 + 9 + 3 * 4 * 3)` becomes *`1445`*.
# * `5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))` becomes *`669060`*.
# * `((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2` becomes *`23340`*.
#
#
# *What do you get if you add up the results of evaluating the homework
# problems using these new rules?*
###

test_input = """1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

test_output = 51 + 46 + 1445 + 669060 + 23340


def find_rpar(expr: List):
    stack = 0
    for i, token in enumerate(expr):
        if token == ")":
            stack -= 1
            if stack == 0:
                return i
        elif token == "(":
            stack += 1
    raise RuntimeError("Unmatched start paren")


def evaluate(expr: List, indent) -> int:
    if expr[0] == "(":
        rpar = find_rpar(expr)
        subexpr = expr[1:rpar]
        lhs, rest = evaluate(subexpr, indent + 2), expr[rpar + 1 :]
    else:
        lhs, rest = expr[0], expr[1:]

    if len(rest) == 0:
        return lhs

    op = rest.pop(0)

    if rest[0] == "(":
        rpar = find_rpar(rest)
        subexpr = rest[1:rpar]
        rhs, rest = evaluate(subexpr, indent + 2), rest[rpar + 1 :]
    else:
        rhs = rest.pop(0)

    if op == "+":
        return evaluate([lhs + rhs] + rest, indent + 2)
    else:
        assert op == "*"
        rhs = evaluate([rhs] + rest, indent + 2)
        return lhs * rhs


def solve(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        tokens = line.replace("(", "( ").replace(")", " )").split()
        tokens = [int(token) if token.isdigit() else token for token in tokens]

        answer += evaluate(tokens, 0)
    return answer
