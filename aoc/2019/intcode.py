from io import TextIOWrapper
import itertools
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    SupportsIndex,
    Tuple,
    overload,
)
from enum import Enum, IntEnum
from collections import namedtuple
from itertools import zip_longest
import operator
import re


class ParamMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Addr:
    addr: int
    mode: ParamMode
    name: Optional[str]

    def __init__(self, addr: int, mode: ParamMode):
        self.addr = addr
        self.mode = mode
        self.name = None

    def code(self):
        if self.name is not None:
            return self.name
        if self.mode is None or self.mode == ParamMode.POSITION:
            return f"mem[{self.addr}]"
        elif self.mode == ParamMode.IMMEDIATE:
            return str(self.addr)
        elif self.mode == ParamMode.RELATIVE:
            return f"mem[bp + {self.addr}]"
        else:
            assert False, f"Invalid param mode {self.mode} for dst"

    def store(self, mem: "Memory", value: int):
        if self.mode is None or self.mode == ParamMode.POSITION:
            mem[self.addr] = value
        elif self.mode == ParamMode.RELATIVE:  # Relative
            mem[self.addr + mem.relative_base] = value
        else:
            assert False, f"Invalid param mode {self.mode} for store"

    def load(self, mem: "Memory") -> int:
        if self.mode is None or self.mode == ParamMode.POSITION:
            return mem[self.addr]
        elif self.mode == ParamMode.IMMEDIATE:
            return self.addr
        elif self.mode == ParamMode.RELATIVE:
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
            assert idx.stop is None or idx.stop < len(self._mem)
        else:
            if idx >= len(self._mem):
                return 0
        return self._mem.__getitem__(idx)

    def __len__(self):
        return len(self._mem)

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


InstrLine = Tuple[int, Instr, List[Addr]]
InstrList = List[InstrLine]


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
            param_modes = [
                ParamMode(int(m))
                for m in f"{self.memory[self.ip] // 100:0{instr.nparams}}"
            ]
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

    def disasm(self) -> str:
        return Disassembler(self.memory).to_string()


class Disassembler:
    class Data(Instr):
        opcode = -1
        mnemonic = "data"

        def __init__(self, first_data: int):
            self.opcode = first_data

        def code(self, params: List[Addr]):
            param_strs = [param.code() for param in params]
            return f"{self.mnemonic} {self.opcode}, {', '.join(param_strs)}"

    def __init__(self, memory: Memory):
        self.memory = memory
        self.disasm()

    def disasm(self) -> InstrList:
        """
        Disassemble the program.

        Assumes there is first a block of code and then (when first encountering a value that is not a legal instruction)
        a block of data.  When there are jumps into data then a new code block is generated at the target address."""

        self.label_idx = 0
        self.jump_dests = {}
        self.var_idx = 0
        self.pvar_idx = 0
        self.addrs = {}
        self.pvar_addrs = {}
        self.code, block_end = self.disasm_at_addr(0)

        while True:
            # Resolve jumps
            new_code_starts = self.find_data_jumps()

            if len(new_code_starts) == 0:
                break
            new_code_start = sorted(new_code_starts)[0]
            self.code.append(self.make_data_instr(block_end, new_code_start))
            new_code, block_end = self.disasm_at_addr(new_code_start)
            self.code += new_code

        if block_end < len(self.memory):
            self.code.append(self.make_data_instr(block_end))

        self.var_block, self.local_var_blocks = self.resolve_vars()

    def to_string(self):
        return self.var_block + "\n".join(
            f"{self.label(ip)}{ip:5} {instr.code(params)}"
            for ip, instr, params in self.code
        )

    def find_data_jumps(self):
        jumps_into_data: Set[int] = set()
        for ip, instr, params in self.code:
            if instr.mnemonic in ["jz", "jnz"]:
                if params[1].mode != ParamMode.IMMEDIATE:
                    if params[1].mode != ParamMode.RELATIVE or params[1].addr != 0:
                        print(
                            f"Warning: dynamic jump from address {ip} to {params[1].code()}"
                        )
                    continue
                self.label_idx += 1
                dest = params[1].addr
                if dest not in self.jump_dests:
                    self.jump_dests[dest] = f"label_{self.label_idx}"
                if not self.addr_is_in_code(dest, expect_jump_target=True):
                    jumps_into_data.add(dest)
                params[1].name = self.jump_dests[dest]

        return jumps_into_data

    def make_data_instr(self, start: int, end=None) -> InstrLine:
        return (
            start,
            Disassembler.Data(self.memory[start]),
            [Addr(a, ParamMode.IMMEDIATE) for a in self.memory[start + 1 : end]],
        )

    def label(self, ip: int):
        labeled = ""
        if ip in self.jump_dests:
            labeled += f"{self.jump_dests[ip]}:\n"
        if ip in self.local_var_blocks:
            labeled += self.local_var_blocks[ip]
        return labeled

    def resolve_vars(self):
        var_block = ""
        local_vars = []
        local_var_blocks = {}
        local_var_addr = 0
        relative_base = 0
        for ip, instr, params in self.code:
            if instr.mnemonic == "base":
                if params[0].mode != ParamMode.IMMEDIATE:
                    print("Warning: Dynamic base pointer adjustment not supported!")
                    continue
                base_adj = params[0].addr
                if base_adj == -len(local_vars):
                    local_vars = []
                    local_var_addr = 0
                elif relative_base != 0:
                    if self.addr_is_in_code(relative_base):
                        print(
                            f"Warning: Relative base pointer {relative_base} is inside code block!"
                        )
                    # Disregard first base pointer set
                    local_vars = [None] * base_adj
                    local_var_addr = ip
                    local_var_blocks[local_var_addr] = ""
                relative_base += base_adj
            for param_idx, p in enumerate(params):
                if p.mode == ParamMode.POSITION:
                    var_block += self.resolve_position_var(
                        p, param_idx == len(params) - 1
                    )
                elif p.mode == ParamMode.RELATIVE and local_var_addr != 0:
                    local_var_blocks[local_var_addr] += self.resolve_relative_var(
                        p, local_vars
                    )
        return var_block, local_var_blocks

    def resolve_position_var(self, p: Addr, is_write: bool) -> str:
        instr = self.instr_at_address(p.addr)
        var_def = ""
        if p.name:
            # This parameter has already been named as a target of another pvar
            return ""
        if instr is not None and instr[1].mnemonic != "data":
            ip, instr, params = instr
            if ip == p.addr:
                print(f"Warning: adressing opcode of {instr.code(params)} at {p.addr}")
                return ""
            if p.addr not in self.pvar_addrs:
                self.pvar_idx += 1
                self.pvar_addrs[p.addr] = f"pvar_{self.pvar_idx}"
            param_modified = params[p.addr - ip - 1]
            param_modified.name = param_modified.code().replace(
                str(param_modified.addr), self.pvar_addrs[p.addr]
            )
            p.name = self.pvar_addrs[p.addr]
        else:
            if p.addr not in self.addrs:
                self.var_idx += 1
                self.addrs[p.addr] = f"var_{self.var_idx}"
                value = self.memory[p.addr]
                var_def = f"@{self.addrs[p.addr]} = mem[{p.addr}]  # {value}\n"

            p.name = self.addrs[p.addr]
        return var_def

    def resolve_relative_var(self, p, local_vars):
        lvar_def = ""
        local_addr = -p.addr
        if local_addr <= 0:
            # New function call; ignore
            return lvar_def

        if local_addr > len(local_vars):
            print(
                f"Warning: Local addressing {-p.addr} outside stack segment of size {len(local_vars)}"
            )
            return ""

        if local_vars[local_addr] is None:
            local_vars[local_addr] = f"lvar_{local_addr}"
            lvar_def = f"@{local_vars[local_addr]} = {p.code()}\n"

        p.name = local_vars[local_addr]
        return lvar_def

    def instr_at_address(self, addr: int) -> Optional[InstrLine]:
        for (ip, instr, p) in self.code:
            if ip <= addr <= ip + len(p):
                return ip, instr, p
        return None

    def addr_is_in_code(self, addr: int, *, expect_jump_target=False) -> bool:
        instr = self.instr_at_address(addr)
        if instr is None:
            return False

        ip, instr, p = instr
        if instr.mnemonic == "data":
            if expect_jump_target:
                print(
                    f"Warning: jump target {addr} is in existing data block (at {ip}-{ip + len(p)})! This is not supperted."
                )
            return False
        if addr != ip and expect_jump_target:
            print(
                f"Warning: address {addr} does not target opcode! ({instr.code(p)} is at {ip})"
            )
        return True

    def disasm_at_addr(self, ip: int) -> Tuple[InstrList, int]:
        code: InstrList = []
        data_start = -1
        while ip < len(self.memory._mem):
            op = self.memory[ip]
            try:
                instr = Instr.get(op % 100)
            except KeyError as e:
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
            code.append((ip, instr, params))

            ip += 1 + instr.nparams

        return code, data_start
