import functools
from io import TextIOBase
import itertools
import logging
from typing import (
    List,
    Optional,
    Set,
    Tuple,
    Callable,
    overload,
)
from enum import Enum
from itertools import zip_longest
import operator

logger = logging.getLogger(__name__)


class PositionParam:
    @staticmethod
    def store(mem: "Memory", addr: int, value: int):
        logger.debug(f"Position store to {addr}: {value}")
        mem[addr] = value

    @staticmethod
    def load(mem: "Memory", addr: int) -> int:
        logger.debug(f"Position load from {addr}: {mem[addr]}")
        return mem[addr]

    @staticmethod
    def code(addr: int) -> str:
        return f"mem[{addr}]"


class ImmediateParam:
    @staticmethod
    def store(mem: "Memory", addr: int, value: int):
        assert False, "Invalid param mode Immediate for store"

    @staticmethod
    def load(mem: "Memory", addr: int) -> int:
        return addr

    @staticmethod
    def code(addr: int) -> str:
        return str(addr)


class RelativeParam:
    @staticmethod
    def store(mem: "Memory", addr: int, value: int):
        logger.debug(f"Relative store to {mem.relative_base} + {addr}: {addr + mem.relative_base} <- {value}")
        mem[addr + mem.relative_base] = value

    @staticmethod
    def load(mem: "Memory", addr: int) -> int:
        value = mem[addr + mem.relative_base]
        logger.debug(f"Relative load from {mem.relative_base} + {addr}: {addr + mem.relative_base} -> {value}")
        return value

    @staticmethod
    def code(addr: int) -> str:
        return f"mem[bp + {addr}]"


class ParamMode(Enum):
    POSITION = (0, PositionParam)
    IMMEDIATE = (1, ImmediateParam)
    RELATIVE = (2, RelativeParam)

    store: Callable[["Memory", int, int], None]
    load: Callable[["Memory", int], int]
    code: Callable[[int], str]

    def __new__(cls, value, mode_cls):
        obj = object.__new__(cls)

        obj._value_ = value
        obj.store = mode_cls.store
        obj.load = mode_cls.load
        obj.code = mode_cls.code

        return obj


class Addr:
    addr: int
    mode: ParamMode
    name: Optional[str]

    def __init__(self, addr: int, mode: ParamMode):
        self.addr = addr
        self.mode = mode
        self.name = None

    def code(self) -> tuple[str, list[str]]:
        if self.name is not None:
            return self.name, [self.mode.code(self.addr)]
        return self.mode.code(self.addr), []

    def store(self, mem: "Memory", value: int):
        self.mode.store(mem, self.addr, value)

    def load(self, mem: "Memory") -> int:
        return self.mode.load(mem, self.addr)


class Memory:
    def __init__(self, mem: List[int]):
        self.__mem = mem
        self._relative_base = 0
        self._protected_ranges = []

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

    def __len__(self):
        return len(self.__mem)

    def grow(self, size):
        assert size < 10 * 2**20, f"Too large block allocation {size/2**20} MiB"

        if size > len(self.__mem):
            self.__mem[len(self.__mem) : size] = itertools.repeat(0, size - len(self.__mem))

    @overload
    def __getitem__(self, idx: int) -> int: ...

    @overload
    def __getitem__(self, idx: slice) -> list[int]: ...

    def __getitem__(self, idx: int | slice) -> int | list[int]:
        return self.__mem[idx]

    def __setitem__(self, idx: int, value: int):
        if idx >= len(self.__mem):
            logger.debug(f"Growing memory to size {idx + 1}")
            self.grow(idx + 1)

        # TODO: optimize?
        if any(start <= idx < end for start, end in self._protected_ranges):
            raise ValueError(f"Attempt to write to protected memory at address {idx}")
        self.__mem[idx] = value

    def protect(self, start_addr: int, end_addr: int):
        self._protected_ranges.append((start_addr, end_addr))


class Instr:
    opcode = None
    mnemonic = "???"
    nparams = 0
    ops = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert cls.opcode not in cls.ops
        cls.ops[cls.opcode] = cls

    def __init__(self, addr: int, machine: "Machine", param_modes: List[ParamMode]):
        self.addr = addr
        self.machine = machine
        self.param_modes = param_modes

    def __str__(self):
        params = [Addr(self.machine.memory[self.addr + i + 1], mode) for i, mode in enumerate(self.param_modes)]
        return f"{self.addr:5} {self.code(params)}"

    def execute(self):
        raise NotImplementedError()

    def store(self, param_index: int, value: int):
        self.param_modes[param_index].store(
            self.machine.memory,
            self.machine.memory[self.addr + param_index + 1],
            value,
        )

    def load(self, param_index: int) -> int:
        return self.param_modes[param_index].load(self.machine.memory, self.machine.memory[self.addr + param_index + 1])

    def code(self, params: List[Addr]) -> str:
        param_tuples = [param.code() for param in params]
        param_strs = [p[0] for p in param_tuples]
        param_annotations = [p for p in param_tuples for p in p[1]]
        return f"{self.mnemonic} {', '.join(param_strs)}  # {', '.join(param_annotations)}"

    @classmethod
    def get(cls, machine: "Machine", ip: int) -> "Instr":
        op = machine.memory[ip]
        try:
            op_cls = cls.ops[op % 100]
        except KeyError as e:
            raise ValueError(f"Invalid opcode {op} at address {ip}") from e
        param_modes = [ParamMode(int(m)) for m in reversed(f"{op // 100:0{op_cls.nparams}}")]

        return op_cls(ip, machine, param_modes)


class Add(Instr):
    opcode = 1
    mnemonic = "add"
    nparams = 3

    def execute(self):
        val = self.load(0) + self.load(1)
        self.store(2, val)


class Mul(Instr):
    opcode = 2
    mnemonic = "mul"
    nparams = 3

    def execute(self):
        self.store(2, self.load(0) * self.load(1))


class Inp(Instr):
    opcode = 3
    mnemonic = "inp"
    nparams = 1

    def execute(self):
        inval = next(self.machine.input_it, None)

        if inval is None:
            # No input, stop and wait for more input
            self.machine.running = False
            self.machine.ip -= 2
        else:
            self.store(0, inval)


class Out(Instr):
    opcode = 4
    mnemonic = "outp"
    nparams = 1

    def execute(self):
        self.machine.output(self.load(0))


class JumpIfTrue(Instr):
    opcode = 5
    mnemonic = "jnz"
    nparams = 2

    def execute(self):
        if self.load(0) != 0:
            self.machine.ip = self.load(1)


class JumpIfFalse(Instr):
    opcode = 6
    mnemonic = "jz"
    nparams = 2

    def execute(self):
        if self.load(0) == 0:
            self.machine.ip = self.load(1)


def unimplemented_compare(x, y) -> bool:
    raise NotImplementedError()


class Compare(Instr):
    opcode = None
    nparams = 3
    compare = unimplemented_compare

    def execute(self):
        if self.__class__.compare(self.load(0), self.load(1)):
            self.store(2, 1)
        else:
            self.store(2, 0)


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

    def execute(self):
        self.machine.memory.relative_base += self.load(0)


class Stop(Instr):
    opcode = 99
    mnemonic = "stop"
    nparams = 0

    def execute(self):
        self.machine.running = False
        self.machine.halted = True


InstrLine = Tuple[int, Instr, List[Addr]]
InstrList = List[InstrLine]


class Machine:
    def __init__(self, memory: List[int]):
        self.memory = Memory(memory)
        self.ip = 0
        self.input_it = iter([])
        self.running = False
        self.halted = False

    @classmethod
    def from_str(cls, mem_str) -> "Machine":
        return cls(list(map(int, mem_str.strip().split(","))))

    @classmethod
    def from_stream(cls, stream: TextIOBase) -> "Machine":
        return cls.from_str(stream.read())

    def reset(self):
        self.ip = 0
        self.halted = False
        self.memory.relative_base = 0

    def run(self, input=[], output_callback: Optional[Callable[[int], None]] = None):
        self.input_it = iter(input)
        out_list: List[int] = []
        self.output = output_callback or (lambda x: out_list.append(x))
        self.running = True
        while self.running:
            instr = self.get_instr(self.ip)
            self.ip += 1
            self.ip += instr.nparams

            logger.debug(f"Executing {instr}")
            instr.execute()
        return None if output_callback else out_list

    @functools.cache
    def get_instr(self, ip: int) -> Instr:
        instr = Instr.get(self, ip)

        return instr

    def protect_memory(self, start_addr: int, end_addr: int):
        self.memory.protect(start_addr, end_addr)

    def disasm(self, extra_code_blocks=[]) -> str:
        return Disassembler(self, extra_code_blocks).to_string()


class Disassembler:
    class Data(Instr):
        opcode = -1
        mnemonic = "data"

        def __init__(self, first_data: int):
            self.opcode = first_data

        def code(self, params: List[Addr]) -> str:
            param_strs = [param.code()[0] for param in params]
            return f"{self.mnemonic} {self.opcode}, {', '.join(param_strs)}"

    def __init__(self, machine: Machine, extra_code_blocks=[]):
        self.machine = machine
        self.memory = machine.memory
        self.disasm(extra_code_blocks)

    def disasm(self, extra_code_blocks=[]):
        """
        Disassemble the program.

        Assumes there is first a block of code and then (when first encountering a value that is not a legal
        instruction) a block of data.  When there are jumps into data then a new code block is generated at
        the target address."""

        self.label_idx = 0
        self.jump_dests = {}
        self.var_idx = 0
        self.pvar_idx = 0
        self.addrs = {}
        self.pvar_addrs = {}
        self.code, block_end = self.disasm_at_addr(0)

        while True:
            # Resolve jumps
            new_code_starts = self.unprocessed_extra_code_blocks(extra_code_blocks) | self.find_data_jumps()

            if len(new_code_starts) == 0:
                break
            new_code_start = sorted(new_code_starts)[0]
            self.code.extend(self.make_data_instrs(block_end, new_code_start))
            new_code, block_end = self.disasm_at_addr(new_code_start)
            self.code += new_code

        if block_end < len(self.memory):
            self.code.extend(self.make_data_instrs(block_end))

        self.var_block, self.local_var_blocks = self.resolve_vars()

    def unprocessed_extra_code_blocks(self, extra_code_blocks):
        return set(b for b in extra_code_blocks if not self.addr_is_in_code(b, expect_jump_target=True))

    def to_string(self):
        code_str = self.var_block + "\n".join(
            f"{self.label(ip)}{ip:5} {instr.code(params)}" for ip, instr, params in self.code
        )

        protect_start = 0
        protect_blocks = []
        for ip, instr, params in self.code:
            if isinstance(instr, Disassembler.Data):
                if ip > protect_start:
                    protect_blocks.append(slice(protect_start, ip))
                protect_start = ip + len(params) + 1
            else:
                pass
        if protect_start < ip:
            protect_blocks.append(slice(protect_start, ip + len(params) + 1))

        for block in protect_blocks:
            print(f"Read-only block: {block}")
        return code_str

    def find_data_jumps(self):
        jumps_into_data: Set[int] = set()
        for ip, instr, params in self.code:
            if instr.mnemonic in ["jz", "jnz"]:
                if params[1].mode != ParamMode.IMMEDIATE:
                    if params[1].mode != ParamMode.RELATIVE or params[1].addr != 0:
                        print(f"Warning: dynamic jump from address {ip} to {params[1].code()}")
                    continue
                self.label_idx += 1
                dest = params[1].addr
                if dest not in self.jump_dests:
                    self.jump_dests[dest] = f"label_{self.label_idx}"
                if not self.addr_is_in_code(dest, expect_jump_target=True):
                    jumps_into_data.add(dest)
                params[1].name = self.jump_dests[dest]

        return jumps_into_data

    def make_data_instrs(self, start: int, end: int | None = None) -> list[InstrLine]:
        end = end or len(self.memory)
        return [
            (
                start,
                Disassembler.Data(self.memory[start]),
                [Addr(a, ParamMode.IMMEDIATE) for a in self.memory[start + 1 : min(end, start + 16)]],
            )
            for start in range(start, end, 16)
        ]

    def label(self, ip: int):
        labeled = ""
        if ip in self.jump_dests:
            labeled += f"{self.jump_dests[ip]}:\n"
        if ip in self.local_var_blocks:
            labeled += self.local_var_blocks[ip]
        return labeled

    def resolve_vars(self):
        var_block = ""
        local_vars: list[str | None] = []
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
                        print(f"Warning: Relative base pointer {relative_base} is inside code block!")
                    # Disregard first base pointer set
                    local_vars = [None] * base_adj
                    local_var_addr = ip
                    local_var_blocks[local_var_addr] = ""
                relative_base += base_adj
            for param_idx, p in enumerate(params):
                if p.mode == ParamMode.POSITION:
                    var_block += self.resolve_position_var(p, param_idx == len(params) - 1)
                elif p.mode == ParamMode.RELATIVE and local_var_addr != 0:
                    local_var_blocks[local_var_addr] += self.resolve_relative_var(p, local_vars)
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
            param_modified.name = param_modified.code()[0].replace(str(param_modified.addr), self.pvar_addrs[p.addr])
            p.name = self.pvar_addrs[p.addr]
        else:
            if p.addr not in self.addrs:
                self.var_idx += 1
                self.addrs[p.addr] = f"var_{self.var_idx}"
                value = self.memory[p.addr]
                var_def = f"@{self.addrs[p.addr]} = mem[{p.addr}]  # {value}\n"

            p.name = self.addrs[p.addr]
        return var_def

    def resolve_relative_var(self, p: Addr, local_vars: list[str | None]):
        lvar_def = ""
        local_addr = -p.addr
        if local_addr <= 0:
            # New function call; ignore
            return lvar_def

        if local_addr > len(local_vars):
            print(f"Warning: Local addressing {-p.addr} outside stack segment of size {len(local_vars)}")
            return ""

        if local_vars[local_addr] is None:
            local_vars[local_addr] = f"lvar_{local_addr}"
            lvar_def = f"@{local_vars[local_addr]} = {p.code()[0]}\n"

        p.name = local_vars[local_addr]
        return lvar_def

    def instr_at_address(self, addr: int) -> Optional[InstrLine]:
        for ip, instr, p in self.code:
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
                    f"Warning: jump target {addr} is in existing data block (at {ip}-{ip + len(p)})!"
                    " This is not supperted."
                )
                # We treat this as if the jump is valid.
                return True
            return False
        if addr != ip and expect_jump_target:
            print(f"Warning: address {addr} does not target opcode! ({instr.code(p)} is at {ip})")
        return True

    def disasm_at_addr(self, ip: int) -> Tuple[InstrList, int]:
        code: InstrList = []
        while ip < len(self.memory):
            op = self.memory[ip]
            try:
                instr = Instr.get(self.machine, ip)
            except ValueError:
                break

            param_modes = [ParamMode(int(i)) for i in f"{op // 100:0{instr.nparams}}"]
            params = [
                Addr(value, mode)
                for value, mode in zip_longest(
                    self.memory[ip + 1 : ip + 1 + instr.nparams],
                    reversed(param_modes),
                )
            ][: instr.nparams]
            code.append((ip, instr, params))

            ip += 1 + instr.nparams

        return code, ip
