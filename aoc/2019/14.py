from io import TextIOWrapper
import math
import functools
import itertools
from typing import Dict

part1_test_input = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

part1_test_output = 2210736


def part1(inp: TextIOWrapper):
    conversions = {}
    for line in inp.readlines():
        inc, outc = line.strip().split(" => ")
        inc = [i.split() for i in inc.split(", ")]
        inc = [(int(inn), inc) for inn, inc in inc]
        outn, outc = outc.split(" ")
        outn = int(outn)
        assert outc not in conversions
        conversions[outc] = (outn, inc)

    answer = ore_required({"FUEL": 1}, conversions)
    return answer


def ore_required(required: Dict, conversions: Dict) -> int:
    ore = 0
    store = {}
    while len(required) > 0:
        reqc, reqn = required.popitem()
        produced, new_req = conversions[reqc]

        stored = store.get(reqc, 0)
        if stored >= reqn:
            store[reqc] = stored - reqn
            reqn = 0
            continue
        elif stored > 0:
            reqn -= stored
            store[reqc] = 0
        units = (reqn + produced - 1) // produced
        surplus = produced * units - reqn
        if surplus > 0:
            store[reqc] = store.get(reqc, 0) + surplus
        for nreqn, nreqc in new_req:
            if nreqc == "ORE":
                ore += nreqn * units
            else:
                required[nreqc] = required.get(nreqc, 0) + nreqn * units
    return ore


part2_test_input = part1_test_input

part2_test_output = 460664


def part2(inp: TextIOWrapper):
    conversions = {}
    for line in inp.readlines():
        inc, outc = line.strip().split(" => ")
        inc = [i.split() for i in inc.split(", ")]
        inc = [(int(inn), inc) for inn, inc in inc]
        outn, outc = outc.split(" ")
        outn = int(outn)
        assert outc not in conversions
        conversions[outc] = (outn, inc)

    one_req = ore_required({"FUEL": 1}, conversions)
    ORE = 1000000000000
    fuel_produced = ORE // one_req
    step = fuel_produced // 2
    while True:
        req = ore_required({"FUEL": fuel_produced}, conversions)
        if req > ORE:
            fuel_produced -= step
            if step > 1:
                step //= 2
        elif req < ORE:
            if step == 1:
                return fuel_produced
            fuel_produced += step
            step //= 2
        else:
            return fuel_produced
