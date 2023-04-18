import sys


class Opcode:
    NOP = 0x00
    JP_XX = 0xC3


class Instr:
    def __init__(self, mnemonic, operands):
        self.mnemonic = mnemonic
        self.operands = operands


def parse(source):
    curr_byte = 0
    instrs = []

    while curr_byte < len(source):
        if source[curr_byte] == Opcode.NOP:
            curr_byte += 1
            instrs.append(Instr("NOP", ()))
        elif source[curr_byte] == Opcode.JP_XX:
            curr_byte += 1
            addr = source[curr_byte]
            curr_byte += 1
            instrs.append(Instr("JP", (addr,)))
        else:
            print("Error: got unknown/unimplemented opcode",
                  f"`{hex(source[curr_byte])}`\n",
                  "Hint: the table of known opcodes is at",
                  "https://clrhome.org/table/")
            sys.exit(1)
    return instrs

