from io import TextIOWrapper
from math import prod
from ..tools import parse_input

part1_test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

part1_test_output = 8


def calc_game(game_id: int, game: str):
    max = (12, 13, 14)
    idx_map = {"red": 0, "green": 1, "blue": 2}

    draws = game.split("; ")
    for draw in draws:
        cols = draw.split(", ")
        for col in cols:
            num, col = col.split(" ")
            num = int(num)
            if max[idx_map[col]] < num:
                return 0
    return int(game_id)


def part1(inp: TextIOWrapper):
    answer = 0

    # for line in inp.readlines():

    # lines = [l for l in inp.readlines()]
    for game_id, game in parse_input(inp, "Game {}: {}"):
        answer += calc_game(game_id, game)

    # lines = [tokens for tokens in parse_input(inp, "")]

    return answer


part2_test_input = part1_test_input

part2_test_output = 2286


def calc_game2(game_id: int, game: str):
    min = [0, 0, 0]
    idx_map = {"red": 0, "green": 1, "blue": 2}

    draws = game.split("; ")
    for draw in draws:
        cols = draw.split(", ")
        for col in cols:
            num, col = col.split(" ")
            num = int(num)
            if min[idx_map[col]] < num:
                min[idx_map[col]] = num
    return prod(min)


def part2(inp: TextIOWrapper):
    answer = 0

    for game_id, game in parse_input(inp, "Game {}: {}"):
        answer += calc_game2(game_id, game)

    return answer
