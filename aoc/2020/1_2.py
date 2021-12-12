def solve(inp):
    entries = set([int(l) for l in inp.readlines()])

    for e in entries:
        for e2 in entries:
            if e is e2:
                continue
            comp = 2020 - e - e2
            if comp in entries:
                print(f"The product of {e}, {e2} and {comp} is {e*e2*comp}")
                return e * e2 * comp
