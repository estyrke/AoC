from io import StringIO, TextIOWrapper
import math
from typing import DefaultDict, List


def dfs(conn, u, e, visited, currentPath, allPaths: List[List[str]]):
    # print("dfs", u, e, currentPath)
    if u.lower() == u:
        # Lowercase
        visited.add(u)

    if u == e:
        allPaths.append(list(currentPath))
        return

    for next in conn[u]:
        if next not in visited:
            currentPath.append(next)
            dfs(conn, next, e, set(visited), currentPath, allPaths)
            currentPath.pop()


def solve(inp: TextIOWrapper):
    answer = None
    test_input = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

    # inp = StringIO(test_input)
    conn = DefaultDict(list)
    for line in inp.readlines():
        s, e = line.strip().split("-")
        conn[s].append(e)
        conn[e].append(s)

    # print(conn)
    visited = set(["start"])
    paths = []
    path = ["start"]
    dfs(conn, "start", "end", visited, path, paths)

    print(len(paths))
    return len(paths)
