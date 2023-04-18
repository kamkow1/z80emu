import sys


class Opcode:
    NOP = 0x00

    JP = 0xC3
    JP_Z = 0xCA
    JP_NZ = 0xC2
    JR = 0x18

    CP = 0xFE
    CP_B = 0xB8

    LD_A = 0x3E


class Instr:
    def __init__(self, mnemonic, numeric_opcode, operands):
        self.mnemonic = mnemonic
        self.numeric_opcode = numeric_opcode
        self.operands = operands

    def __repr__(self):
        field1 = f"mnemonic = {self.mnemonic}"
        field2 = f"numeric_opcode = {hex(self.numeric_opcode)}"
        field3 = f"operands = {self.operands}"
        return f"Instr({field1}, {field2}, {field3})"


def parse(source):
    curr_byte = 0
    instrs = []

    while curr_byte < len(source):
        if source[curr_byte] == Opcode.NOP:
            curr_byte += 1
            instrs.append(Instr("NOP", Opcode.NOP, ()))
        elif source[curr_byte] == Opcode.JP:
            curr_byte += 1
            addr = source[curr_byte]
            curr_byte += 1
            instrs.append(Instr("JP", Opcode.JP, (addr,)))
        elif source[curr_byte] == Opcode.JP_Z:
            curr_byte += 1
            addr = source[curr_byte]
            curr_byte += 2
            instrs.append(Instr("JP Z", Opcode.JP_Z, (addr,)))
        elif source[curr_byte] == Opcode.JP_NZ:
            curr_byte += 1
            addr = source[curr_byte]
            curr_byte += 2
            instrs.append(Instr("JP NZ", Opcode.JP_NZ, (addr,)))
        elif source[curr_byte] == Opcode.JR:
            curr_byte += 1
            offset = source[curr_byte]
            curr_byte += 1
            instrs.append(Instr("JR", Opcode.JR, (offset,)))
            curr_byte += 1
        elif source[curr_byte] == Opcode.CP:
            curr_byte += 1
            value = source[curr_byte]
            curr_byte += 1
            instrs.append(Instr("CP", Opcode.CP, (value,)))
        elif source[curr_byte] == Opcode.CP_B:
            curr_byte += 1
            instrs.append(Instr("CP B", Opcode.CP_B, ()))
        elif source[curr_byte] == Opcode.LD_A:
            curr_byte += 1
            value = source[curr_byte]
            curr_byte += 1
            instrs.append(Instr("LD A", Opcode.LD_A, (value,)))
        else:
            print("Error: got unknown/unimplemented opcode",
                  f"`{hex(source[curr_byte])}`\n",
                  "Hint: the table of known opcodes is at",
                  "https://clrhome.org/table/")
            sys.exit(1)
    return instrs

