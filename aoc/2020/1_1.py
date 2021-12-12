def solve(inp):
    entries = set([int(l) for l in inp.readlines()])

    for e in entries:
        comp = 2020 - e
        if comp in entries:
            print(f"The product of {e} and {comp} is {e*comp}")
            return e * comp
