from io import TextIOWrapper
import itertools
from typing import List, NamedTuple, Sequence, SupportsIndex, Tuple, overload
from enum import Enum
from collections import namedtuple
from itertools import zip_longest
import operator
import re


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Addr:
    addr: int
    mode: ParamMode

    def __init__(self, addr: int, mode: ParamMode):
        self.addr = addr
        self.mode = mode

    def code(self):
        if self.mode is None or self.mode == 0:
            return f"mem[{self.addr}]"
        elif self.mode == 1:  # Immediate
            return str(self.addr)
        elif self.mode == 2:  # Relative
            return f"mem[bp + {self.addr}]"
        else:
            assert False, f"Invalid param mode {self.mode} for dst"

    def store(self, mem: "Memory", value: int):
        if self.mode is None or self.mode == 0:
            mem[self.addr] = value
        elif self.mode == 2:  # Relative
            mem[self.addr + mem.relative_base] = value
        else:
            assert False, f"Invalid param mode {self.mode} for store"

    def load(self, mem: "Memory") -> int:
        if self.mode is None or self.mode == 0:  # position mode
            return mem[self.addr]
        elif self.mode == 1:  # Immediate
            return self.addr
        elif self.mode == 2:  # Relative
            return mem[self.addr + mem.relative_base]
        else:
            assert False, f"Invalid param mode {self.mode} for load"


class Memory:
    def __init__(self, mem: List[int]):
        self._mem = mem
        self._relative_base = 0

    def store(self, dst: Addr, value: int):
        dst.store(self, value)

    def load(self, src: Addr) -> int:
        return src.load(self)

    @property
    def relative_base(self):
        return self._relative_base

    @relative_base.setter
    def relative_base(self, base: int):
        self._relative_base = base

    @overload
    def __getitem__(self, idx: slice) -> List[int]:
        ...

    @overload
    def __getitem__(self, idx: SupportsIndex) -> int:
        ...

    def __getitem__(self, idx):  # type: ignore
        if isinstance(idx, slice):
            assert idx.stop < len(self._mem)
        else:
            if idx >= len(self._mem):
                return 0
        return self._mem.__getitem__(idx)

    def grow(self, size):
        assert size < 10 * 2 ** 20, f"Too large block allocation {size/2**20} MiB"

        if size > len(self._mem):
            self._mem[len(self._mem) : size] = itertools.repeat(
                0, size - len(self._mem)
            )

    def __setitem__(self, idx: int, value: int):
        self.grow(idx + 1)
        return self._mem.__setitem__(idx, value)


class Instr:
    opcode = None
    mnemonic = "???"
    nparams = 0
    ops = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert cls.opcode not in cls.ops
        cls.ops[cls.opcode] = cls

    def execute(self, machine: "Machine", params: List[Addr]):
        raise NotImplementedError()

    def code(self, params: List[Addr]):
        param_strs = [param.code() for param in params]
        return f"{self.mnemonic} {', '.join(param_strs)}"

    @classmethod
    def get(cls, opcode) -> "Instr":
        return cls.ops[opcode]()


class Add(Instr):
    opcode = 1
    mnemonic = "add"
    nparams = 3

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.store(params[2], memory.load(params[0]) + memory.load(params[1]))


class Mul(Instr):
    opcode = 2
    mnemonic = "mul"
    nparams = 3

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.store(params[2], memory.load(params[0]) * memory.load(params[1]))


class Inp(Instr):
    opcode = 3
    mnemonic = "inp"
    nparams = 1

    def execute(self, machine: "Machine", params: List[Addr]):

        memory = machine.memory
        inval = next(machine.input_it, None)

        if inval is None:
            # No input, stop and wait for more input
            machine.running = False
            machine.ip -= 2
        else:
            memory.store(params[0], inval)


class Out(Instr):
    opcode = 4
    mnemonic = "outp"
    nparams = 1

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        machine.output.append(memory.load(params[0]))


class JumpIfTrue(Instr):
    opcode = 5
    mnemonic = "jnz"
    nparams = 2

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        if memory.load(params[0]) != 0:
            machine.ip = memory.load(params[1])


class JumpIfFalse(Instr):
    opcode = 6
    mnemonic = "jz"
    nparams = 2

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        if memory.load(params[0]) == 0:
            machine.ip = memory.load(params[1])


def unimplemented_compare(x, y) -> bool:
    raise NotImplementedError()


class Compare(Instr):
    opcode = None
    nparams = 3
    compare = unimplemented_compare

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        if self.__class__.compare(memory.load(params[0]), memory.load(params[1])):
            memory.store(params[2], 1)
        else:
            memory.store(params[2], 0)


class CompareLt(Compare):
    opcode = 7
    mnemonic = "cmplt"
    compare = operator.lt


class CompareEq(Compare):
    opcode = 8
    mnemonic = "cmpeq"
    compare = operator.eq


class AdjustBase(Instr):
    opcode = 9
    mnemonic = "base"
    nparams = 1

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.relative_base += memory.load(params[0])


class Stop(Instr):
    opcode = 99
    mnemonic = "stop"
    nparams = 0

    def execute(self, machine: "Machine", params: List[Addr]):
        machine.running = False
        machine.halted = True


class Machine:
    def __init__(self, memory: List[int]):
        self.memory = Memory(memory)
        self.ip = 0
        self.input_it = iter([])
        self.output = []
        self.running = False
        self.halted = False

    @classmethod
    def from_str(cls, mem_str) -> "Machine":
        return cls(list(map(int, mem_str.strip().split(","))))

    @classmethod
    def from_stream(cls, stream: TextIOWrapper) -> "Machine":
        return cls.from_str(stream.read())

    def reset(self):
        self.ip = 0
        self.halted = False
        self.memory.relative_base = 0

    def run(self, input=[]):
        self.input_it = iter(input)
        self.output = []
        self.running = True
        while self.running:
            instr = Instr.get(self.memory[self.ip] % 100)
            param_modes = list(
                map(int, f"{self.memory[self.ip] // 100:0{instr.nparams}}")
            )
            self.ip += 1
            params = [
                Addr(value, mode)
                for value, mode in zip_longest(
                    self.memory[self.ip : self.ip + instr.nparams],
                    reversed(param_modes),
                )
            ]

            self.ip += instr.nparams

            instr.execute(self, params)
        return self.output

    def disasm(self, data_chunk_len: int = 8) -> str:
        """
        Disassemble the program.

        Assumes there is first a block of code and then (when first encountering a value that is not a legal instruction)
        a block of data."""
        code = []
        data_start = 0
        ip = 0
        while ip < len(self.memory._mem):
            op = self.memory[ip]
            try:
                instr = Instr.get(op % 100)
            except KeyError as e:
                # print(f"Illegal instruction {op % 100} at {ip}")
                data_start = ip

                break

            param_modes = list(map(int, f"{op // 100:0{instr.nparams}}"))
            params = [
                Addr(value, mode)
                for value, mode in zip_longest(
                    self.memory[ip + 1 : ip + 1 + instr.nparams],
                    reversed(param_modes),
                )
            ][: instr.nparams]
            code.append(f"{ip:5} {instr.code(params)}")

            ip += 1 + instr.nparams

        code = "\n".join(code)

        # Resolve memory addresses
        addrs = re.findall("mem\\[(\\d+)\\]", code)
        addrs = set(int(m) for m in addrs)
        var_block = ""
        for i, addr in enumerate(sorted(addrs)):
            if addr > data_start:
                value = self.memory[addr]
                var_block += f"@var_{i} = mem[{addr}]  # {value}\n"
                code = code.replace(f"mem[{addr}]", f"var_{i}")
            else:
                print(f"Warning: addressing {addr} inside code block!")
        code = var_block + code

        # Resolve jumps
        jumps = re.findall("jn?z (\\w+), (\\w+)", code)
        jump_dests = {int(m[1]): f"label_{i}" for i, m in enumerate(jumps)}
        for dest, label in jump_dests.items():
            code = re.sub(
                f"(jn?z \\w+, ){dest}$", f"\\1{label}", code, flags=re.MULTILINE
            )
            code = re.sub(f"^(\\s*{dest} )", f"{label}:\n\\1", code, flags=re.MULTILINE)

        # Append data block
        while data_start < len(self.memory._mem):
            chunk = [
                f"{x:02}"
                for x in self.memory._mem[data_start : data_start + data_chunk_len]
            ]
            code += f"\n{data_start:5} data {', '.join(chunk)}"
            data_start += data_chunk_len
        return code
