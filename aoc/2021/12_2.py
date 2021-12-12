from io import StringIO, TextIOWrapper
import math
from typing import DefaultDict, List


def dfs(
    conn,
    u,
    e,
    visited: DefaultDict,
    currentPath,
    allPaths: List[str],
    small_cave: str,
):
    # print("dfs", u, e, currentPath)
    if u.lower() == u:
        # Lowercase
        visited[u] += 1

    if u == e:
        allPaths.append("-".join(currentPath))
        return

    for next in conn[u]:
        if visited[next] == 0 or (next == small_cave and visited[next] < 2):
            currentPath.append(next)
            dfs(conn, next, e, visited.copy(), currentPath, allPaths, small_cave)
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

    inp2 = StringIO(test_input)
    conn = DefaultDict(list)
    for line in inp.readlines():
        s, e = line.strip().split("-")
        conn[s].append(e)
        conn[e].append(s)

    # print(conn)
    all_paths = set()
    for small_cave in [
        k for k in conn.keys() if k.lower() == k and k not in ["start", "end"]
    ]:
        visited = DefaultDict(int)
        visited["start"] = 1
        paths = []
        path = ["start"]

        dfs(conn, "start", "end", visited, path, paths, small_cave)
        all_paths.update(paths)

    print(len(all_paths))
    return len(all_paths)
