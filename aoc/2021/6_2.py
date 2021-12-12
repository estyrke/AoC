# ## --- Part Two ---
#
# Suppose the lanternfish live forever and have unlimited food and
# space. Would they take over the entire ocean?
#
# After 256 days in the example above, there would be a total of
# `*26984457539*` lanternfish!
#
# *How many lanternfish would there be after 256 days?*

### BEGIN CODE
# * After one day, its internal timer would become `2`.
# * After another day, its internal timer would become `1`.
# * After another day, its internal timer would become `0`.
# * After another day, its internal timer would reset to `6`, and it
# would create a *new* lanternfish with an internal timer of `8`.
# * After another day, the first lanternfish would have an internal
# timer of `5`, and the second lanternfish would have an internal timer
# of `7`.


def solve(inp):
    fish = [int(l) for l in inp.readline().split(",")]
    # fish = [3, 4, 3, 1, 2]
    fish = [fish.count(d) for d in range(9)]
    print(fish)
    for d in range(256):
        day_0 = fish.pop(0)
        fish[6] += day_0
        fish.append(day_0)
        # print(fish)
    answer = sum(fish)
    return answer
