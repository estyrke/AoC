from io import TextIOWrapper
import math
import functools
import itertools

part1_test_input = """"""

part1_test_output = None


def part1(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        other, me = line.split()
        if other == "A" and me == "Y":
            answer += 6
        elif other == "B" and me == "Z":
            answer += 6
        elif other == "C" and me == "X":
            answer += 6
        elif ord(me) - ord(other) == ord("X") - ord("A"):
            answer += 3
        answer += ord(me) - ord("X") + 1

    return answer


part2_test_input = part1_test_input

part2_test_output = None


def part2(inp: TextIOWrapper):
    answer = 0

    for line in inp.readlines():
        other, me = line.split()
        if me == "X":
            if other == "A":
                me = "Z"
            elif other == "B":
                me = "X"
            elif other == "C":
                me = "Y"
        elif me == "Y":
            me = chr(ord(other) + (ord("X") - ord("A")))
        else:
            if other == "A":
                me = "Y"
            elif other == "B":
                me = "Z"
            else:
                me = "X"
        if other == "A" and me == "Y":
            answer += 6
        elif other == "B" and me == "Z":
            answer += 6
        elif other == "C" and me == "X":
            answer += 6
        elif ord(me) - ord(other) == ord("X") - ord("A"):
            answer += 3
        answer += ord(me) - ord("X") + 1
    return answer
