from io import TextIOWrapper
import math
from typing import DefaultDict, Set

###
# ## --- Part Two ---
#
# Now that you've isolated the inert ingredients, you should have enough
# information to figure out which ingredient contains which allergen.
#
# In the above example:
#
# * `mxmxvkd` contains `dairy`.
# * `sqjhc` contains `fish`.
# * `fvjkl` contains `soy`.
#
#
# Arrange the ingredients *alphabetically by their allergen* and
# separate them by commas to produce your *canonical dangerous
# ingredient list*. (There should *not be any spaces* in your canonical
# dangerous ingredient list.) In the above example, this would be
# *`mxmxvkd,sqjhc,fvjkl`*.
#
# Time to stock your raft with supplies. *What is your canonical
# dangerous ingredient list?*
###

test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

test_output = "mxmxvkd,sqjhc,fvjkl"

import functools
import operator


def solve(inp: TextIOWrapper):
    answer = None

    allergens: Set[str] = set()
    ingredients: Set[str] = set()
    foods = []
    for line in inp.readlines():
        i, a = line.strip().split(" (contains ")
        i = set(i.split())
        a = set(a.strip(")").split(", "))
        ingredients |= i
        allergens |= a
        foods.append((i, a))

    possible_ingredients_per_allergen = DefaultDict(lambda: set(ingredients))
    for ings, alls in foods:
        for a in alls:
            possible_ingredients_per_allergen[a] &= ings

    allergen_by_ingredient = []
    cont = True
    while cont:

        for all, ings in possible_ingredients_per_allergen.items():
            if len(ings) == 1:
                ing = next(iter(ings))
                allergen_by_ingredient.append((all, ing))
                possible_ingredients_per_allergen = {
                    k: v - {ing} for k, v in possible_ingredients_per_allergen.items()
                }
                break
        else:
            cont = False

    allergen_by_ingredient.sort()
    return ",".join([a[1] for a in allergen_by_ingredient])
