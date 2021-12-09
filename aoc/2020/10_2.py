from io import TextIOWrapper
import math

###
# ## --- Part Two ---
#
# To completely determine whether you have enough adapters, you'll need
# to figure out how many different ways they can be arranged. Every
# arrangement needs to connect the charging outlet to your device. The
# previous rules about when adapters can successfully connect still
# apply.
#
# The first example above (the one that starts with `16`, `10`, `15`)
# supports the following arrangements:
#
#
# ```
# (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
#
# ```
#
# (The charging outlet and your device's built-in adapter are shown in
# parentheses.) Given the adapters from the first example, the total
# number of arrangements that connect the charging outlet to your device
# is *`8`*.
#
# The second example above (the one that starts with `28`, `33`, `18`)
# has many arrangements. Here are a few:
#
#
# ```
# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)
#
# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)
#
# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)
#
# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)
#
# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)
#
# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 46, 48, 49, (52)
#
# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 46, 49, (52)
#
# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 47, 48, 49, (52)
#
# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 47, 49, (52)
#
# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 48, 49, (52)
#
# ```
#
# In total, this set of adapters can connect the charging outlet to your
# device in *`19208`* distinct arrangements.
#
# You glance back down at your bag and try to remember why you brought
# so many adapters; there must be *more than a trillion* valid ways to
# arrange them! Surely, there must be an efficient way to count the
# arrangements.
#
# *What is the total number of distinct ways you can arrange the
# adapters to connect the charging outlet to your device?*
###


def solve(inp: TextIOWrapper):
    adapters = [
        28,
        33,
        18,
        42,
        31,
        14,
        46,
        20,
        48,
        47,
        24,
        23,
        49,
        45,
        19,
        38,
        39,
        11,
        1,
        32,
        25,
        35,
        8,
        17,
        7,
        9,
        4,
        2,
        34,
        10,
        3,
    ]
    # adapters = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    adapters = [int(l) for l in inp.readlines()]

    adapters.sort()
    print(adapters)
    perms = [1]
    device_jolts = max(adapters) + 3
    for i in range(1, device_jolts):
        if i not in adapters:
            perms.append(0)
            continue

        perms.append(sum(perms[max(i - 3, 0) : i]))

    print(perms)
    answer = sum(perms[-3:])
    return answer
