from io import TextIOWrapper
import itertools
from typing import List, NamedTuple, Sequence, SupportsIndex, Tuple, overload
from enum import Enum
from collections import namedtuple
from itertools import zip_longest
import operator


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Addr:
    addr: int
    mode: ParamMode

    def __init__(self, addr: int, mode: ParamMode):
        self.addr = addr
        self.mode = mode


class Memory:
    def __init__(self, mem: List[int]):
        self._mem = mem
        self._relative_base = 0

    def store(self, dst: Addr, value: int):
        if dst.mode is None or dst.mode == 0:
            self[dst.addr] = value
        elif dst.mode == 2:  # Relative
            self[dst.addr + self._relative_base] = value
        else:
            assert False, f"Invalid param mode {dst.mode} for dst"

    def load(self, src: Addr) -> int:
        if src.mode is None or src.mode == 0:  # position mode
            return self[src.addr]
        elif src.mode == 1:  # Immediate
            return src.addr
        elif src.mode == 2:  # Relative
            return self[src.addr + self._relative_base]
        else:
            assert False, f"Invalid param mode {src.mode} for src"

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
    nparams = 0
    ops = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert cls.opcode not in cls.ops
        cls.ops[cls.opcode] = cls

    def execute(self, machine: "Machine", params: List[Addr]):
        raise NotImplementedError()

    @classmethod
    def get(cls, opcode) -> "Instr":
        return cls.ops[opcode]()


class Add(Instr):
    opcode = 1
    nparams = 3

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.store(params[2], memory.load(params[0]) + memory.load(params[1]))


class Mul(Instr):
    opcode = 2
    nparams = 3

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.store(params[2], memory.load(params[0]) * memory.load(params[1]))


class Inp(Instr):
    opcode = 3
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
    nparams = 1

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        machine.output.append(memory.load(params[0]))


class JumpIfTrue(Instr):
    opcode = 5
    nparams = 2

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        if memory.load(params[0]) != 0:
            machine.ip = memory.load(params[1])


class JumpIfFalse(Instr):
    opcode = 6
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
    compare = operator.lt


class CompareEq(Compare):
    opcode = 8
    compare = operator.eq


class AdjustBase(Instr):
    opcode = 9
    nparams = 1

    def execute(self, machine: "Machine", params: List[Addr]):
        memory = machine.memory
        memory.relative_base += memory.load(params[0])


class Stop(Instr):
    opcode = 99
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
