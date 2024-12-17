from io import StringIO, TextIOBase
import sys

part1_test_input = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

part1_test_output = "4,6,3,5,6,3,5,2,1,0"


def disasm(prog):
    def operand_str(operand):
        if operand < 4:
            return f"{operand}"
        return chr(65 + operand - 4)

    for ip in range(0, len(prog), 2):
        opcode = prog[ip]
        operand = prog[ip + 1]
        match opcode:
            case 0:
                print(f"{ip:2d}: adv {operand_str(operand)}")
            case 1:
                print(f"{ip:2d}: bxl {operand}")
            case 2:
                print(f"{ip:2d}: bst {operand_str(operand)}")
            case 3:
                print(f"{ip:2d}: jnz {operand}")
            case 4:
                print(f"{ip:2d}: bxc ({operand})")
            case 5:
                print(f"{ip:2d}: out {operand_str(operand)}")
            case 6:
                print(f"{ip:2d}: bdv {operand_str(operand)}")
            case 7:
                print(f"{ip:2d}: cdv {operand_str(operand)}")
            case _:
                print(f"Invalid opcode {opcode} at position {ip}")


def part1(inp: TextIOBase):
    answer = None

    regs, prog = inp.read().split("\n\n")
    regs = [int(l.split(": ")[1]) for l in regs.split("\n")]
    prog = [int(l) for l in prog.split(": ")[1].split(",")]

    print(regs, prog)
    disasm(prog)
    out = execute_program(regs, prog)

    answer = ",".join(map(str, out))
    return answer


def execute_program(regs, prog):
    ip = 0
    out = []
    while True:
        opcode = prog[ip]
        operand = prog[ip + 1]
        match opcode:
            case 0:  # ADV
                assert operand != 7
                if operand < 4:
                    regs[0] = regs[0] // 2**operand
                else:
                    regs[0] = regs[0] // 2 ** regs[operand - 4]
            case 1:  # BXL
                regs[1] = regs[1] ^ operand
            case 2:  # BST
                assert operand != 7
                if operand < 4:
                    regs[1] = operand % 8
                else:
                    regs[1] = regs[operand - 4] % 8
            case 3:  # JNZ
                if regs[0] != 0:
                    ip = operand
                    continue
            case 4:  # BXC
                regs[1] = regs[1] ^ regs[2]
            case 5:  # OUT
                assert operand != 7
                if operand < 4:
                    out.append(operand)
                else:
                    out.append(regs[operand - 4] % 8)
            case 6:  # BDV
                assert operand != 7
                if operand < 4:
                    regs[1] = regs[0] // 2**operand
                else:
                    regs[1] = regs[0] // 2 ** regs[operand - 4]
            case 7:  # CDV
                assert operand != 7
                if operand < 4:
                    regs[2] = regs[0] // 2**operand
                else:
                    regs[2] = regs[0] // 2 ** regs[operand - 4]
            case _:
                raise ValueError(f"Invalid opcode {opcode} at position {ip}")
        ip += 2
        if ip >= len(prog):
            break
    return out


part2_test_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

part2_test_output = 117440


def part2(inp: TextIOBase):
    answer = None

    regs, prog = inp.read().split("\n\n")
    regs = [int(l.split(": ")[1]) for l in regs.split("\n")]
    prog = [int(l) for l in prog.split(": ")[1].split(",")]

    print(regs, prog)
    disasm(prog)
    ip = 0
    out = []

    def reg_name(operand):
        return chr(ord("a") + operand)

    disasm_python(prog, ip, out, reg_name)

    choices = {tuple()}
    for pos in range(len(prog) - 1, -1, -1):
        new_choices = set()
        for bits in range(8):
            for rest in choices:
                a = 0
                for r in reversed(rest):
                    a += r
                    a <<= 3
                a += bits

                out = execute_program([a, 0, 0], prog)
                if out == prog[pos:]:
                    # print(pos, a, out, prog[-pos - 1 :])
                    new_choices.add((bits, *rest))
        assert new_choices, f"no choices at pos {pos}, rest {choices}"
        choices = new_choices
        print("choices", choices)

    answer = None
    for choice in choices:
        test_ans = 0
        for i, r in enumerate(reversed(choice)):
            test_ans <<= 3
            test_ans += r
        if answer is None or test_ans < answer:
            answer = test_ans

    # Verify
    assert answer
    out = execute_program([answer, 0, 0], prog)
    print(out)
    print(prog)
    assert out == prog

    return answer


def disasm_python(prog, ip, out, reg_name):
    for ip in range(0, len(prog), 2):
        opcode = prog[ip]
        operand = prog[ip + 1]
        match opcode:
            case 0:  # ADV
                assert operand != 7
                if operand < 4:
                    out.append(f"a = a // {2**operand}")
                else:
                    out.append(f"a = a // 2 ** {reg_name(operand - 4)}")
            case 1:  # BXL
                out.append(f"b = b ^ {operand}")
            case 2:  # BST
                assert operand != 7
                if operand < 4:
                    out.append(f"b = {operand % 8}")
                else:
                    out.append(f"b = {reg_name(operand - 4)} % 8")
            case 3:  # JNZ
                out[operand:] = [f"    {o}" for o in out[operand:]]
                out.insert(operand, "while True:")
                out.append("    if a == 0: break")
            case 4:  # BXC
                out.append("b = b ^ c")
            case 5:  # OUT
                assert operand != 7
                if operand < 4:
                    out.append(f"out.append({operand})")
                else:
                    out.append(f"out.append({reg_name(operand-4)} % 8)")
            case 6:  # BDV
                assert operand != 7
                if operand < 4:
                    out.append(f"b = a // {2**operand}")
                else:
                    out.append(f"b = a // 2 ** {reg_name(operand-4)}")
            case 7:  # CDV
                assert operand != 7
                if operand < 4:
                    out.append(f"c = a // {2**operand}")
                else:
                    out.append(f"c = a // 2 ** {reg_name(operand-4)}")
            case _:
                raise ValueError(f"Invalid opcode {opcode} at position {ip}")

    print("\n".join(out))


if __name__ == "__main__":
    inp = sys.stdin.read()
    print(part1(StringIO(inp)))
    print(part2(StringIO(inp)))
