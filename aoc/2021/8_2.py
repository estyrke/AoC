from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# Through a little deduction, you should now be able to determine the
# remaining digits. Consider again the first example above:
#
#
# ```
# acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
# cdfeb fcadb cdfeb cdbaf
# ```
#
# After some careful analysis, the mapping between signal wires and
# segments only make sense in the following configuration:
#
#
# ```
#  dddd
# e    a
# e    a
#  ffff
# g    b
# g    b
#  cccc
#
# ```
#
# So, the unique signal patterns would correspond to the following
# digits:
#
# * `acedgfb`: `8`
# * `cdfbe`: `5`
# * `gcdfa`: `2`
# * `fbcad`: `3`
# * `dab`: `7`
# * `cefabd`: `9`
# * `cdfgeb`: `6`
# * `eafb`: `4`
# * `cagedb`: `0`
# * `ab`: `1`
#
#
# Then, the four digits of the output value can be decoded:
#
# * `cdfeb`: `*5*`
# * `fcadb`: `*3*`
# * `cdfeb`: `*5*`
# * `cdbaf`: `*3*`
#
#
# Therefore, the output value for this entry is `*5353*`.
#
# Following this same process for each entry in the second, larger
# example above, the output value of each entry can be determined:
#
# * `fdgacbe cefdb cefbgd gcbe`: `8394`
# * `fcgedb cgb dgebacf gc`: `9781`
# * `cg cg fdcagb cbg`: `1197`
# * `efabcd cedba gadfec cb`: `9361`
# * `gecf egdcabf bgf bfgea`: `4873`
# * `gebdcfa ecba ca fadegcb`: `8418`
# * `cefg dcbef fcge gbcadfe`: `4548`
# * `ed bcgafe cdgba cbgef`: `1625`
# * `gbdfcae bgc cg cgb`: `8717`
# * `fgae cfgab fg bagce`: `4315`
#
#
# Adding all of the output values in this larger example produces
# `*61229*`.
#
# For each entry, determine all of the wire/segment connections and
# decode the four-digit output values. *What do you get if you add up
# all of the output values?*
###


def decode_value(in_vals, out_vals):
    len_mapping = {}
    print(in_vals, out_vals)
    for i, inv in enumerate(in_vals):
        if len(inv) not in len_mapping:
            len_mapping[len(inv)] = []
        len_mapping[len(inv)].append(i)

    mapping = {}
    rev_map = {}
    mapping[in_vals[len_mapping[2][0]]] = 1
    rev_map[1] = set(in_vals[len_mapping[2][0]])

    mapping[in_vals[len_mapping[3][0]]] = 7
    rev_map[7] = set(in_vals[len_mapping[3][0]])

    mapping[in_vals[len_mapping[4][0]]] = 4
    rev_map[4] = set(in_vals[len_mapping[4][0]])

    mapping[in_vals[len_mapping[7][0]]] = 8
    rev_map[8] = set(in_vals[len_mapping[7][0]])

    top_elem = rev_map[7].difference(rev_map[1])

    bot_right_elem = None
    for zero_six_nine_idx in len_mapping[6]:
        zero_six_nine = set(in_vals[zero_six_nine_idx])
        if len(zero_six_nine.intersection(rev_map[1])) != 2:
            mapping[in_vals[zero_six_nine_idx]] = 6
            rev_map[6] = zero_six_nine
            bot_right_elem = zero_six_nine.intersection(rev_map[1]).pop()
            break

    top_right_elem = (rev_map[1] - set([bot_right_elem])).pop()

    for two_three_five_idx in len_mapping[5]:
        two_three_five = set(in_vals[two_three_five_idx])
        if bot_right_elem not in two_three_five:
            mapping[in_vals[two_three_five_idx]] = 2
            rev_map[2] = two_three_five
        elif top_right_elem not in two_three_five:
            mapping[in_vals[two_three_five_idx]] = 5
            rev_map[5] = two_three_five
        else:
            mapping[in_vals[two_three_five_idx]] = 3
            rev_map[3] = two_three_five

    bot_left_elem = (rev_map[2] - rev_map[3] - rev_map[5]).pop()
    for zero_six_nine_idx in len_mapping[6]:
        zero_six_nine = set(in_vals[zero_six_nine_idx])
        if bot_left_elem in zero_six_nine and zero_six_nine != rev_map[6]:
            mapping[in_vals[zero_six_nine_idx]] = 0
            rev_map[0] = zero_six_nine
        elif zero_six_nine != rev_map[6]:
            mapping[in_vals[zero_six_nine_idx]] = 9
            rev_map[9] = zero_six_nine

    sorted_mapping = {str(sorted(k)): v for k, v in mapping.items()}
    sorted_out_vals = [str(sorted(list(v))) for v in out_vals]
    print(mapping, rev_map)
    return (
        1000 * sorted_mapping[sorted_out_vals[0]]
        + 100 * sorted_mapping[sorted_out_vals[1]]
        + 10 * sorted_mapping[sorted_out_vals[2]]
        + sorted_mapping[sorted_out_vals[3]]
    )


def solve(inp: TextIOWrapper):
    answer = 0
    # for line in [
    #    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    # ]:
    for line in inp.readlines():
        in_vals, out_vals = line.strip().split("|")
        in_vals = in_vals.split()
        out_vals = out_vals.split()
        answer += decode_value(in_vals, out_vals)

    return answer
