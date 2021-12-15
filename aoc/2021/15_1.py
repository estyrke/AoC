from io import TextIOWrapper
import math
from typing import Dict, Optional, Tuple

###
# # ## --- Day 15: Chiton ---
#
# You've almost reached the exit of the cave, but the walls are getting
# closer together. Your submarine can barely still fit, though; the main
# problem is that the walls of the cave are covered in
# [chitons](https://en.wikipedia.org/wiki/Chiton), and it would be best
# not to bump any of them.
#
# The cavern is large, but has a very low ceiling, restricting your
# motion to two dimensions. The shape of the cavern resembles a square;
# a quick scan of chiton density produces a map of *risk level*
# throughout the cave (your puzzle input). For example:
#
#
# ```
# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581
#
# ```
#
# You start in the top left position, your destination is the bottom
# right position, and you cannot move diagonally. The number at each
# position is its *risk level*; to determine the total risk of an entire
# path, add up the risk levels of each position you *enter* (that is,
# don't count the risk level of your starting position unless you enter
# it; leaving it adds no risk to your total).
#
# Your goal is to find a path with the *lowest total risk*. In this
# example, a path with the lowest total risk is highlighted here:
#
#
# ```
# *1*163751742
# *1*381373672
# *2136511*328
# 369493*15*69
# 7463417*1*11
# 1319128*13*7
# 13599124*2*1
# 31254216*3*9
# 12931385*21*
# 231194458*1*
#
# ```
#
# The total risk of this path is `*40*` (the starting position is never
# entered, so its risk is not counted).
#
# *What is the lowest total risk of any path from the top left to the
# bottom right?*
###

test_input = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

test_output = 40


def neighbors(pos, rows, cols):
    n = []
    if pos[0] > 0:
        n.append((pos[0] - 1, pos[1]))
    if pos[1] > 0:
        n.append((pos[0], pos[1] - 1))
    if pos[0] < rows - 1:
        n.append((pos[0] + 1, pos[1]))
    if pos[1] < cols - 1:
        n.append((pos[0], pos[1] + 1))

    return n


def solve(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    risks = [[int(r) for r in l.strip()] for l in inp.readlines()]

    rows = len(risks)
    cols = len(risks[0])
    shortest_paths: Dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], int]] = {
        (0, 0): (None, 0)
    }
    current_node = (0, 0)
    visited = set()

    while current_node != (rows - 1, cols - 1):
        visited.add(current_node)
        destinations = neighbors(current_node, rows, cols)
        weight_to_current = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = risks[next_node[0]][next_node[1]] + weight_to_current
            if next_node not in shortest_paths or shortest_paths[next_node][1] > weight:
                shortest_paths[next_node] = (current_node, weight)

        next_destinations = {
            node: shortest_paths[node] for node in shortest_paths if node not in visited
        }
        assert next_destinations
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    return shortest_paths[current_node][1]
