from typing import List, NamedTuple, Sequence, SupportsIndex, Tuple, overload
from enum import Enum
from collections import namedtuple
from itertools import zip_longest
import operator


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


Addr = namedtuple("Addr", "addr mode")


class Memory:
    def __init__(self, mem: List[int]):
        self._mem = mem

    def store(self, dst: Addr, value: int):
        if dst[1] is None or dst[1] == 0:
            self._mem[dst[0]] = value
        else:
            assert False, f"Invalid param mode {dst[1]} for dst"

    def load(self, src: Addr) -> int:
        if src[1] is None or src[1] == 0:  # position mode
            return self._mem[src[0]]
        elif src[1] == 1:  # Immediate
            return src[0]
        else:
            assert False, f"Invalid param mode {src[1]} for src"

    @overload
    def __getitem__(self, idx: slice) -> List[int]:
        ...

    @overload
    def __getitem__(self, idx: SupportsIndex) -> int:
        ...

    def __getitem__(self, idx):  # type: ignore
        return self._mem.__getitem__(idx)


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
    def from_str(cls, mem_str):
        return cls(list(map(int, mem_str.strip().split(","))))

    def reset(self):
        self.ip = 0
        self.halted = False

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
