import fileinput
from io import StringIO, TextIOBase
from z3 import Optimize, Int, Sum, IntNumRef

part1_test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

part1_test_output = 7


def bfs(btns: list[list[int]], target: tuple[bool, ...]):
    q = [((False,) * len(target), [(False,) * len(target)])]
    seen = set()
    while q:
        state, path = q.pop(0)
        if state in seen:
            continue
        seen.add(state)
        if state == target:
            return len(path) - 1
        for btn in btns:
            new_state = tuple(not l if i in btn else l for i, l in enumerate(state))
            if new_state not in seen:
                q.append((new_state, path + [new_state]))
    raise RuntimeError(f"No path for target {target} using {btns}")


def part1(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        pars = line.strip().split()
        btn = pars[0].strip("[]")
        wiring = [[int(y) for y in x.strip("()").split(",")] for x in pars[1:-1]]
        _jolt = [int(x) for x in pars[-1].strip("{}").split(",")]

        answer += bfs(wiring, tuple(c == "#" for c in btn))

    return answer


part2_test_input = part1_test_input

part2_test_output = 33


def part2(inp: TextIOBase):
    answer = 0

    for line in inp.readlines():
        pars = line.strip().split()
        wiring = [[int(y) for y in x.strip("()").split(",")] for x in pars[1:-1]]
        jolt = [int(x) for x in pars[-1].strip("{}").split(",")]

        incs: list[list[int]] = []
        for w in wiring:
            inc = [0] * len(jolt)
            for pos in w:
                inc[pos] = 1

            incs.append(inc)

        s = Optimize()
        presses = [Int(f"btn{i}") for i, inc in enumerate(incs)]
        for p in presses:
            s.add(p >= 0)
        for i, j in enumerate(jolt):
            p = []
            for press, inc in zip(presses, incs, strict=True):
                if inc[i]:
                    p.append(press)
            s.add(Sum(p) == j)
        s.minimize(Sum(presses))
        s.check()
        m = s.model()  # 3 5 4 7
        for p in presses:
            val = m[p]
            assert isinstance(val, IntNumRef), type(val)
            answer += val.as_long()

    return answer


if __name__ == "__main__":
    inp = "".join(fileinput.input(encoding="utf-8"))
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
