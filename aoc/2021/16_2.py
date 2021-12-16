from io import TextIOWrapper
import math
import functools

###
# ## --- Part Two ---
#
# Now that you have the structure of your transmission decoded, you can
# calculate the value of the expression it represents.
#
# Literal values (type ID `4`) represent a single number as described
# above. The remaining type IDs are more interesting:
#
# * Packets with type ID `0` are *sum* packets - their value is the sum
# of the values of their sub-packets. If they only have a single sub-
# packet, their value is the value of the sub-packet.
# * Packets with type ID `1` are *product* packets - their value is the
# result of multiplying together the values of their sub-packets. If
# they only have a single sub-packet, their value is the value of the
# sub-packet.
# * Packets with type ID `2` are *minimum* packets - their value is the
# minimum of the values of their sub-packets.
# * Packets with type ID `3` are *maximum* packets - their value is the
# maximum of the values of their sub-packets.
# * Packets with type ID `5` are *greater than* packets - their value is
# *1* if the value of the first sub-packet is greater than the value of
# the second sub-packet; otherwise, their value is *0*. These packets
# always have exactly two sub-packets.
# * Packets with type ID `6` are *less than* packets - their value is
# *1* if the value of the first sub-packet is less than the value of the
# second sub-packet; otherwise, their value is *0*. These packets always
# have exactly two sub-packets.
# * Packets with type ID `7` are *equal to* packets - their value is *1*
# if the value of the first sub-packet is equal to the value of the
# second sub-packet; otherwise, their value is *0*. These packets always
# have exactly two sub-packets.
#
#
# Using these rules, you can now work out the value of the outermost
# packet in your BITS transmission.
#
# For example:
#
# * `C200B40A82` finds the sum of `1` and `2`, resulting in the value
# `*3*`.
# * `04005AC33890` finds the product of `6` and `9`, resulting in the
# value `*54*`.
# * `880086C3E88112` finds the minimum of `7`, `8`, and `9`, resulting
# in the value `*7*`.
# * `CE00C43D881120` finds the maximum of `7`, `8`, and `9`, resulting
# in the value `*9*`.
# * `D8005AC2A8F0` produces `1`, because `5` is less than `15`.
# * `F600BC2D8F` produces `0`, because `5` is not greater than `15`.
# * `9C005AC2F8F0` produces `0`, because `5` is not equal to `15`.
# * `9C0141080250320F1802104A08` produces `1`, because `1` + `3` = `2` *
# `2`.
#
#
# *What do you get if you evaluate the expression represented by your
# hexadecimal-encoded BITS transmission?*
###

test_input = """8A004A801A8002F478"""
test_input = """620080001611562C8802118E34"""
test_input = """9C0141080250320F1802104A08"""
"""A0016C880162017C3686B18A3D4780"""

test_output = 16
test_output = 12
test_output = 1
31


def hex_to_binary(data: str):
    for i in data:
        b = bin(int(i, 16))[2:]
        yield "0" * (4 - len(b)) + b


def solve(inp: TextIOWrapper):
    answer = None

    # for line in inp.readlines():
    # lines = [l for l in inp.readlines()]
    data = inp.read().strip()
    data = "".join(hex_to_binary(data))
    answer = 0
    while True:
        if len(data) == 0 or len(data) < 8 and int(data, 2) == 0:
            break
        data, vsum = parse(data)
        answer += vsum
    return answer


import operator


def parse(data: str):
    if len(data) == 0:
        print("EMPTY")
        return "", 0
    version, data = int(data[:3], 2), data[3:]
    type, data = int(data[:3], 2), data[3:]
    # print("version + type", version, type)

    res = 0
    if type == 4:
        num = ""
        while True:
            chunk, data = data[:5], data[5:]
            cont = chunk[0]
            num += chunk[1:]
            if cont == "0":
                break
        res = int(num, 2)
        # print(num)
    else:
        if type == 0:
            op = operator.add
        elif type == 1:
            op = operator.mul
        elif type == 2:
            op = min
        elif type == 3:
            op = max
        elif type == 5:
            op = lambda x, y: 1 if x > y else 0
        elif type == 6:
            op = lambda x, y: 1 if x < y else 0
        else:
            assert type == 7
            op = lambda x, y: 1 if x == y else 0
        ltype, data = data[0], data[1:]
        operands = []

        if ltype == "0":
            length, data = int(data[:15], 2), data[15:]
            # print("ltype 0", length)
            subdata, data = data[:length], data[length:]
            while len(subdata) > 0:
                subdata, vs = parse(subdata)
                operands.append(vs)
        else:
            n_sub_packets, data = int(data[:11], 2), data[11:]
            # print("ltype 1", n_sub_packets)
            for i in range(n_sub_packets):
                data, vs = parse(data)
                operands.append(vs)

        res = functools.reduce(op, operands[1:], operands[0])
    # padding = len(data) % 4
    return data, res
