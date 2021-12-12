from typing import Dict
import re

# ## --- Part Two ---
#
# The line is moving more quickly now, but you overhear airport security
# talking about how passports with invalid data are getting through.
# Better add some data validation, quick!
#
# You can continue to ignore the `cid` field, but each other field has
# strict rules about what values are valid for automatic validation:
#
# * `byr` (Birth Year) - four digits; at least `1920` and at most
# `2002`.
# * `iyr` (Issue Year) - four digits; at least `2010` and at most
# `2020`.
# * `eyr` (Expiration Year) - four digits; at least `2020` and at most
# `2030`.
# * `hgt` (Height) - a number followed by either `cm` or `in`:         +
# If `cm`, the number must be at least `150` and at most `193`.
# + If `in`, the number must be at least `59` and at most `76`.
# * `hcl` (Hair Color) - a `#` followed by exactly six characters
# `0`-`9` or `a`-`f`.
# * `ecl` (Eye Color) - exactly one of: `amb` `blu` `brn` `gry` `grn`
# `hzl` `oth`.
# * `pid` (Passport ID) - a nine-digit number, including leading zeroes.
# * `cid` (Country ID) - ignored, missing or not.
#
#
# Your job is to count the passports where all required fields are both
# *present* and *valid* according to the above rules. Here are some
# example values:
#
#
# ```
# byr valid:   2002
# byr invalid: 2003
#
# hgt valid:   60in
# hgt valid:   190cm
# hgt invalid: 190in
# hgt invalid: 190
#
# hcl valid:   #123abc
# hcl invalid: #123abz
# hcl invalid: 123abc
#
# ecl valid:   brn
# ecl invalid: wat
#
# pid valid:   000000001
# pid invalid: 0123456789
#
# ```
#
# Here are some invalid passports:
#
#
# ```
# eyr:1972 cid:100
# hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926
#
# iyr:2019
# hcl:#602927 eyr:1967 hgt:170cm
# ecl:grn pid:012533040 byr:1946
#
# hcl:dab227 iyr:2012
# ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277
#
# hgt:59cm ecl:zzz
# eyr:2038 hcl:74454a iyr:2023
# pid:3556412378 byr:2007
#
# ```
#
# Here are some valid passports:
#
#
# ```
# pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
# hcl:#623a2f
#
# eyr:2029 ecl:blu cid:129 byr:1989
# iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm
#
# hcl:#888785
# hgt:164cm byr:2001 iyr:2015 cid:88
# pid:545766238 ecl:hzl
# eyr:2022
#
# iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
#
# ```
#
# Count the number of *valid* passports - those that have all required
# fields *and valid values*. Continue to treat `cid` as optional. *In
# your batch file, how many passports are valid?*


def valid_fields(fields: Dict[str, str]) -> bool:
    try:
        # * `byr` (Birth Year) - four digits; at least `1920` and at most `2002`.
        assert valid_byr(fields)
        # * `iyr` (Issue Year) - four digits; at least `2010` and at most `2020`.
        assert valid_iyr(fields)
        # * `eyr` (Expiration Year) - four digits; at least `2020` and at most `2030`.
        assert valid_eyr(fields)
        # * `hgt` (Height) - a number followed by either `cm` or `in`:
        #    If `cm`, the number must be at least `150` and at most `193`.
        #    If `in`, the number must be at least `59` and at most `76`.
        assert valid_hgt(fields)
        # * `hcl` (Hair Color) - a `#` followed by exactly six characters `0`-`9` or `a`-`f`.
        assert valid_hcl(fields)
        # * `ecl` (Eye Color) - exactly one of: `amb` `blu` `brn` `gry` `grn` `hzl` `oth`.
        assert valid_ecl(fields)
        # * `pid` (Passport ID) - a nine-digit number, including leading zeroes.
        assert valid_pid(fields)
        # * `cid` (Country ID) - ignored, missing or not.
    except AssertionError:
        return False

    return True


def valid_pid(fields):
    return re.match(r"\d{9}$", fields["pid"]) is not None


def valid_ecl(fields):
    return fields["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def valid_hcl(fields):
    return re.match(r"#[0-9a-f]{6}$", fields["hcl"], re.IGNORECASE) is not None


def valid_eyr(fields):
    return 2020 <= int(fields["eyr"]) <= 2030


def valid_iyr(fields):
    return 2010 <= int(fields["iyr"]) <= 2020


def valid_byr(fields):
    return 1920 <= int(fields["byr"]) <= 2002


def valid_hgt(fields):
    hgt = re.match(r"(\d+)(in|cm)$", fields["hgt"], re.IGNORECASE)
    if not hgt:
        return False

    return (hgt.group(2).lower() == "cm" and 150 <= int(hgt.group(1)) <= 193) or (
        hgt.group(2).lower() == "in" and 59 <= int(hgt.group(1)) <= 76
    )


def solve(inp):

    answer = 0
    required_fields = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    fields = {}
    passports = []
    num = 0
    for line in inp.readlines() + ["\n"]:
        if line.strip() == "":
            num += 1
            passports.append(fields)
            fields = {}
        else:
            fields.update({f.split(":")[0]: f.split(":")[1] for f in line.split()})

    passports.sort(key=lambda p: p.get("pid", ""))
    for p in passports:
        if required_fields.intersection(p.keys()) == required_fields and valid_fields(
            p
        ):
            answer += 1

    print(answer, num)
    if answer == 110:
        answer = None
    return answer
