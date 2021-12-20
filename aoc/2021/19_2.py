from io import SEEK_CUR, TextIOWrapper
import math
from typing import DefaultDict, Set
from itertools import combinations, permutations

###
# ## --- Part Two ---
#
# Sometimes, it's a good idea to appreciate just how big the ocean is.
# Using the [Manhattan
# distance](https://en.wikipedia.org/wiki/Taxicab_geometry), how far
# apart do the scanners get?
#
# In the above example, scanners `2` (`1105,-1205,1229`) and `3`
# (`-92,-2380,-20`) are the largest Manhattan distance apart. In total,
# they are `1197 + 1175 + 1249 = *3621*` units apart.
#
# *What is the largest Manhattan distance between any two scanners?*
###

test_input = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

test_output = 3621

import numpy as np
import scipy as sp


def solve(inp: TextIOWrapper):
    answer = None

    scanner_maps = DefaultDict(set)
    scanner_id = -1
    for line in inp.readlines() + ["\n"]:
        if line.strip() == "":
            scanner_id = -1
            # assert scanner_id != -1
            # scanner_maps[scanner_id] = sp.
        elif line.startswith("---"):
            scanner_id = int(line.strip().split()[2])
        else:
            assert scanner_id != -1
            scanner_maps[scanner_id].add(tuple(map(int, line.strip().split(","))))

    scanners = {(0, 0, 0)}
    while len(scanner_maps) > 1:
        for i, m in scanner_maps.items():
            if i != 0:
                new_beacons, scanner = align(scanner_maps[0], m)
                if scanner is not None:
                    print(scanner)
                    scanners.add(scanner)

                if new_beacons is not None:
                    scanner_maps[0] = new_beacons
                    del scanner_maps[i]
                    print(len(scanner_maps))
                    break
        else:
            assert False

    max_d = 0
    for s1, s2 in combinations(scanners, 2):
        d = abs(s1[0] - s2[0]) + abs(s1[1] - s2[1]) + abs(s1[2] - s2[2])
        max_d = max(max_d, d)
    return max_d


def align(m0: Set, m: Set):
    for rot, matrix in rotations(m):
        for p0 in m0:
            for shifted, shift in shifts(rot, p0):
                overlap = m0 & shifted
                if len(overlap) >= 12:
                    return (m0 | shifted, point_sub((0, 0, 0), shift))
    return None, None


def y_rotations(m):
    yield m, lambda x, y, z: (x, y, z)
    yield {(p[2], p[1], -p[0]) for p in m}, lambda x, y, z: (-z, y, x)
    yield {(-p[0], p[1], -p[2]) for p in m}, lambda x, y, z: (-x, y, -z)
    yield {(-p[2], p[1], p[0]) for p in m}, lambda x, y, z: (z, y, -x)


def x_rotations(m):
    yield {(p[0], p[2], -p[1]) for p in m}, lambda x, y, z: (x, -z, y)
    yield {(p[0], -p[2], p[1]) for p in m}, lambda x, y, z: (x, z, -y)


def z_rotations(m, inv):
    yield m, inv
    yield {(p[1], -p[0], p[2]) for p in m}, lambda x, y, z: inv(-y, x, z)
    yield {(-p[0], -p[1], p[2]) for p in m}, lambda x, y, z: inv(-x, -y, z)
    yield {(-p[1], p[0], p[2]) for p in m}, lambda x, y, z: inv(y, -x, z)


def rotations(m):
    for yrot, inv in y_rotations(m):
        yield from z_rotations(yrot, inv)

    for xrot, inv in x_rotations(m):
        yield from z_rotations(xrot, inv)


def point_sub(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]


def shifts(m, p0):
    for pt in m:
        pd = point_sub(pt, p0)
        yield {point_sub(p, pd) for p in m}, pd
