from io import TextIOWrapper
import math
from functools import lru_cache

###
# ## --- Part Two ---
#
# Now that you're warmed up, it's time to play the real game.
#
# A second compartment opens, this time labeled *Dirac dice*. Out of it
# falls a single three-sided die.
#
# As you experiment with the die, you feel a little strange. An
# informational brochure in the compartment explains that this is a
# *quantum die*: when you roll it, the universe *splits into multiple
# copies*, one copy for each possible outcome of the die. In this case,
# rolling the die always splits the universe into *three copies*: one
# where the outcome of the roll was `1`, one where it was `2`, and one
# where it was `3`.
#
# The game is played the same as before, although to prevent things from
# getting too far out of hand, the game now ends when either player's
# score reaches at least `*21*`.
#
# Using the same starting positions as in the example above, player 1
# wins in `*444356092776315*` universes, while player 2 merely wins in
# `341960390180808` universes.
#
# Using your given starting positions, determine every possible outcome.
# *Find the player that wins in more universes; in how many universes
# does that player win?*
###

test_input = """Player 1 starting position: 4
Player 2 starting position: 8"""

test_output = 444356092776315


def solve(inp: TextIOWrapper):
    starting = [int(x.strip().split()[-1]) for x in inp.readlines()]

    num_outcomes = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    def board_pos(p):
        return (p - 1) % 10 + 1

    @lru_cache(maxsize=None)
    def num_ways_to_have_points_by_turn(player, points, turn, position):
        if turn == 0 and points == 0 and position == starting[player]:
            return 1
        if turn <= 0 or points <= 0:
            return 0

        total = 0
        for o, n in num_outcomes.items():
            total += n * num_ways_to_have_points_by_turn(
                player, points - position, turn - 1, board_pos(position - o)
            )
        return total

    def num_wins_on_turn(player, turn):
        total = 0
        for starting_points in range(11, 21):
            for roll, num in num_outcomes.items():
                for starting_position in range(1, 11):
                    ending_position = board_pos(starting_position + roll)
                    ending_points = starting_points + ending_position
                    if ending_points >= 21:
                        total += num * num_ways_to_have_points_by_turn(
                            player, starting_points, turn - 1, starting_position
                        )
        return total

    def num_non_wins_on_turn(player, turn):
        total = 0
        for points in range(21):
            for position in range(1, 11):
                total += num_ways_to_have_points_by_turn(player, points, turn, position)
        return total

    wins1 = []
    wins2 = []

    for i in range(1, 20):
        wins1.append(num_wins_on_turn(0, i) * num_non_wins_on_turn(1, i - 1))
        wins2.append(num_wins_on_turn(1, i) * num_non_wins_on_turn(0, i))

    print(wins1)
    print(wins2)
    return max(sum(wins1), sum(wins2))
