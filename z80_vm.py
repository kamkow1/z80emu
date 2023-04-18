import sys
import z80_parser


class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


class VM:
    def __init__(self):
        self.registers = {}
        self.registers["A"] = Z80Register("A", "Accumulator")
        self.registers["B"] = Z80Register("B", "Accumulator")
        self.registers["D"] = Z80Register("D", "Accumulator")
        self.registers["H"] = Z80Register("H", "Accumulator")
        self.registers["C"] = Z80Register("C", "Carry flag")
        self.registers["Z"] = Z80Register("Z", "Zero flag")
        self.registers["S"] = Z80Register("S", "Sign flag")
        self.registers["N"] = Z80Register("N", "Add/Sub flag")
        self.registers["P/V"] = Z80Register("P/V", "Parity/overflow flag")
        self.registers["H"] = Z80Register("H", "Half carry flag")
        self.registers["IX"] = Z80Register("IX", "Index register")
        self.registers["IY"] = Z80Register("IY", "Index register")
        self.registers["I"] = Z80Register("I", "Interrupt vector")
        self.registers["R"] = Z80Register("R", "Memory refresh")
        self.registers["SP"] = Z80Register("SP", "Stack pointer")
        self.registers["PC"] = Z80Register("PC", "Program counter")

    def setup_flags_and_pc(self):
        self.registers["PC"].value = 0
        self.registers["C"].value = False
        self.registers["Z"].value = False
        self.registers["S"].value = False
        self.registers["N"].value = False
        self.registers["P/V"].value = False
        self.registers["H"].value = False

    def dump_registers(self, iter):
        print(f"REGISTER STATE (ITERATION {iter}):")
        print("-------------------------------------")
        for key, reg in self.registers.items():
            print(f"{key} = {reg.value}")
        print("-------------------------------------")

    def instr_cp(self, value):
        a = self.registers["A"].value
        result = value - a
        if a == result:
            self.registers["Z"].value = True
        else:
            self.registers["Z"].value = False

        if result < 0:
            # unsigned
            if a < result:
                self.registers["C"].value = True
            elif a >= result:
                self.registers["C"].value = False
        else:
            # signed
            self.registers["S"].value = True
            if a < result:
                self.registers["P/V"].value = False
            elif a >= result:
                self.registers["P/V"].value = True

    def exec(self, instrs):
        self.setup_flags_and_pc()

        while self.registers["PC"].value < len(instrs):
            curr_instr = instrs[self.registers["PC"].value]

            if curr_instr.numeric_opcode == z80_parser.Opcode.NOP:
                self.registers["PC"].value += 1
            elif curr_instr.numeric_opcode == z80_parser.Opcode.JP:
                self.registers["PC"].value = curr_instr.operands[0]
            elif curr_instr.numeric_opcode == z80_parser.Opcode.JP_Z:
                if self.registers["Z"].value:
                    print(self.registers["Z"].value)
                    self.registers["PC"].value = curr_instr.operands[0]
                else:
                    self.registers["PC"].value += 1
            elif curr_instr.numeric_opcode == z80_parser.Opcode.JP_NZ:
                if not self.registers["Z"].value:
                    self.registers["PC"].value = curr_instr.operands[0]
                else:
                    self.registers["PC"].value += 1
            elif curr_instr.numeric_opcode == z80_parser.Opcode.CP:
                value = curr_instr.operands[0]
                self.instr_cp(value)
                self.registers["PC"].value += 1
            elif curr_instr.numeric_opcode == z80_parser.Opcode.CP_B:
                self.instr_cp(self.registers["B"].value)
                self.registers["PC"].value += 1
            elif curr_instr.numeric_opcode == z80_parser.Opcode.LD_A:
                value = curr_instr.operands[0]
                self.registers["A"].value = value
                self.registers["PC"].value += 1
            else:
                print("Error: got parsed, but unhandled instruction",
                      f"`{instrs[self.registers['PC']]}`")
                sys.exit(1)

