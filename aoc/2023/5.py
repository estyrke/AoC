from io import StringIO, TextIOWrapper
import sys

part1_test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

part1_test_output = 35


def part1(inp: TextIOWrapper):
    maps = {}
    map = None
    map_name = None
    seeds = []
    for line in inp.readlines():
        if line.startswith("seeds:"):
            seeds = [int(x) for x in line.split(":")[1].strip().split()]
        elif "map:" in line:
            if map:
                maps[map_name] = sorted(map, key=lambda x: x[1])
            map_name = line.split()[0]
            map = []
        elif len(line.strip()) and map is not None:
            map.append([int(x) for x in line.strip().split()])
    if map:
        maps[map_name] = sorted(map, key=lambda x: x[1])
    # print(maps)
    # lines = [l for l in inp.readlines()]
    # for tokens in parse_input(inp, ""):
    # lines = [tokens for tokens in parse_input(inp, "")]
    dsts = []
    for s in seeds:
        dst = s
        for map_name in [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]:
            map = maps[map_name]
            for dst_start, src_start, length in map:
                if src_start <= dst < src_start + length:
                    dst = dst_start + dst - src_start
                    break
                if dst < src_start:
                    # No more matches
                    break

        dsts.append(dst)

    return min(dsts)


part2_test_input = part1_test_input

part2_test_output = 46


def part2(inp: TextIOWrapper):
    maps = {}
    map = None
    map_name = None
    seeds = []
    for line in inp.readlines():
        if line.startswith("seeds:"):
            seeds = [int(x) for x in line.split(":")[1].strip().split()]
        elif "map:" in line:
            if map:
                maps[map_name] = sorted(map, key=lambda x: x[1])
            map_name = line.split()[0]
            map = []
        elif len(line.strip()) and map is not None:
            map.append([int(x) for x in line.strip().split()])
    if map:
        maps[map_name] = sorted(map, key=lambda x: x[1])
    ranges = list(zip(seeds[0::2], seeds[1::2]))
    for map_name in [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]:
        map = maps[map_name]

        new_ranges = []
        for low, num in ranges:
            curr = low
            for i, (dst_start, src_start, length) in enumerate(map):
                if curr < src_start:
                    curr_end = min(low + num, src_start)
                    new_ranges.append((curr, curr_end - curr))
                    curr = curr_end
                if curr < src_start + length:
                    curr_end = min(low + num, src_start + length)
                    new_ranges.append((dst_start + curr - src_start, curr_end - curr))
                    curr = curr_end
                if curr >= low + num:
                    # No more matches
                    break
            if curr < low + num:
                new_ranges.append((curr, low + num - curr))
        ranges = sorted(new_ranges)

    return ranges[0][0]


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
