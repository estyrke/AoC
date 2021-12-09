from io import TextIOWrapper
import math
from typing import List, Optional

###
# ## --- Part Two ---
#
# For some reason, the sea port's computer system still can't
# communicate with your ferry's docking program. It must be using
# *version 2* of the decoder chip!
#
# A version 2 decoder chip doesn't modify the values being written at
# all. Instead, it acts as a [memory address
# decoder](https://www.youtube.com/watch?v=PvfhANgLrm4). Immediately
# before a value is written to memory, each bit in the bitmask modifies
# the corresponding bit of the destination *memory address* in the
# following way:
#
# * If the bitmask bit is `0`, the corresponding memory address bit is
# *unchanged*.
# * If the bitmask bit is `1`, the corresponding memory address bit is
# *overwritten with `1`*.
# * If the bitmask bit is `X`, the corresponding memory address bit is
# *floating*.
#
#
# A *floating* bit is not connected to anything and instead fluctuates
# unpredictably. In practice, this means the floating bits will take on
# *all possible values*, potentially causing many memory addresses to be
# written all at once!
#
# For example, consider the following program:
#
#
# ```
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
#
# ```
#
# When this program goes to write to memory address `42`, it first
# applies the bitmask:
#
#
# ```
# address: 000000000000000000000000000000101010  (decimal 42)
# mask:    000000000000000000000000000000X1001X
# result:  000000000000000000000000000000*X1*10*1X*
#
# ```
#
# After applying the mask, four bits are overwritten, three of which are
# different, and two of which are *floating*. Floating bits take on
# every possible combination of values; with two floating bits, four
# actual memory addresses are written:
#
#
# ```
# 000000000000000000000000000000*0*1101*0*  (decimal 26)
# 000000000000000000000000000000*0*1101*1*  (decimal 27)
# 000000000000000000000000000000*1*1101*0*  (decimal 58)
# 000000000000000000000000000000*1*1101*1*  (decimal 59)
#
# ```
#
# Next, the program is about to write to memory address `26` with a
# different bitmask:
#
#
# ```
# address: 000000000000000000000000000000011010  (decimal 26)
# mask:    00000000000000000000000000000000X0XX
# result:  00000000000000000000000000000001*X*0*XX*
#
# ```
#
# This results in an address with three floating bits, causing writes to
# *eight* memory addresses:
#
#
# ```
# 00000000000000000000000000000001*0*0*00*  (decimal 16)
# 00000000000000000000000000000001*0*0*01*  (decimal 17)
# 00000000000000000000000000000001*0*0*10*  (decimal 18)
# 00000000000000000000000000000001*0*0*11*  (decimal 19)
# 00000000000000000000000000000001*1*0*00*  (decimal 24)
# 00000000000000000000000000000001*1*0*01*  (decimal 25)
# 00000000000000000000000000000001*1*0*10*  (decimal 26)
# 00000000000000000000000000000001*1*0*11*  (decimal 27)
#
# ```
#
# The entire 36-bit address space still begins initialized to the value
# 0 at every address, and you still need the sum of all values left in
# memory at the end of the program. In this example, the sum is *`208`*.
#
# Execute the initialization program using an emulator for a version 2
# decoder chip. *What is the sum of all values left in memory after it
# completes?*
###


def mask_addrs(value: int, mask: List[Optional[str]]):
    value_bits = []
    for i in range(36):
        value_bits.insert(0, value % 2)
        value >>= 1

    addrs = [[]]
    for i, mb in enumerate(mask):
        if mb is None:
            # Duplicate existing list
            addrs = [addr + [0] for addr in addrs] + [addr + [1] for addr in addrs]
        else:
            addrs = [addr + [mb if mb == 1 else value_bits[i]] for addr in addrs]

    return [
        sum([b * 2 ** (35 - i) for i, b in enumerate(res_bits)]) for res_bits in addrs
    ]


def solve(inp: TextIOWrapper):
    mask: List[Optional[str]] = [None] * 36
    mem = {}
    mask_map = {"0": 0, "1": 1, "X": None}
    for line in inp.readlines():
        op, value = line.strip().split(" = ")
        if op == "mask":
            mask = [mask_map[m] for m in value]
        else:
            in_addr = int(op[4:-1])
            addrs = mask_addrs(in_addr, mask)
            for addr in addrs:
                mem[addr] = int(value)

    return sum(mem.values())
