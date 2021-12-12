import re


def solve(inp):
    valid = 0
    for line in inp.readlines():
        m = re.match(r"(\d+)-(\d+) (\w): (\w+)", line)
        if not m:
            raise RuntimeError("Failed to match " + line)
        min, max, char, pwd = m.groups()

        if pwd.count(char) >= int(min) and pwd.count(char) <= int(max):
            valid += 1
    return valid
