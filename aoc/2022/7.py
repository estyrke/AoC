from collections import defaultdict
from io import TextIOWrapper
import math
import functools
import itertools
from pprint import pprint
from ..tools import parse_input

part1_test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

part1_test_output = 95437


def get_size(dir: str, tree) -> int:
    res = 0
    for size, file in tree[dir]:
        if size == "dir":
            res += get_size(dir + "/" + file, tree)
        else:
            res += size
    return res


def part1(inp: TextIOWrapper):
    answer = 0

    dir = []
    dirs = defaultdict(list)
    in_ls = False
    for line in inp.readlines():
        line = line.strip()
        if line.startswith("$ "):
            in_ls = False

        if line.startswith("$ cd .."):
            dir.pop()
        elif line.startswith("$ cd "):
            dir.extend(line[5:].split("/"))
        elif line.startswith("$ ls"):
            in_ls = True
        elif in_ls:
            size, file = line.split()
            if size == "dir":
                dirs["/".join(dir)].append(("dir", file))
            else:
                dirs["/".join(dir)].append((int(size), file))
        else:
            assert False

    pprint(dirs)
    for k, v in dirs.items():
        s = get_size(k, dirs)
        if s < 100000:
            answer += s

    return answer


part2_test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

part2_test_output = 24933642


def part2(inp: TextIOWrapper):
    answer = 0

    dir = []
    dirs = defaultdict(list)
    in_ls = False
    for line in inp.readlines():
        line = line.strip()
        if line.startswith("$ "):
            in_ls = False

        if line.startswith("$ cd .."):
            dir.pop()
        elif line.startswith("$ cd "):
            dir.extend(line[5:].split("/"))
        elif line.startswith("$ ls"):
            in_ls = True
        elif in_ls:
            size, file = line.split()
            if size == "dir":
                dirs["/".join(dir)].append(("dir", file))
            else:
                dirs["/".join(dir)].append((int(size), file))
        else:
            assert False

    used = get_size("/", dirs)
    unused = 70000000 - used
    print("unused", unused)
    smallest = 70000000
    for k, v in dirs.items():
        s = get_size(k, dirs)
        if s + unused >= 30000000 and s < smallest:
            smallest = s

    return smallest
