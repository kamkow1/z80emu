import sys


class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


BIN_TO_STR_REGS = {
        0b111: "A",
        0b000: "B",
        0b001: "C",
        0b010: "D",
        0b011: "E",
        0b100: "H",
        0b101: "L"}


class VM:
    def increment_pc(self):
        self.registers["PC"].value += 1

    def handler_nop(self, opcode):
        pass

    def handler_jp_n_n(self, opcode):
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.registers["PC"].value = high_byte << 8 | low_byte

    def handler_ld_r8_n(self, opcode):
        reg = (opcode >> 3) & 7
        if reg not in BIN_TO_STR_REGS:
            print(f"Error: encoutnered an unknown register `{hex(reg)}`")
            sys.exit(1)

        data = self.ram[self.registers["PC"].value]
        self.increment_pc()
        self.registers[BIN_TO_STR_REGS[reg]].value = data

    def handler_ld_r16_n_n(self, opcode):
        reg = (opcode >> 4) & 3
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()

        if reg == 0:
            # BC
            self.registers["B"].value = high_byte
            self.registers["C"].value = low_byte
        elif reg == 2:
            # HL
            self.registers["H"].value = high_byte
            self.registers["L"].value = low_byte

    def __init__(self, source):
        # init ram
        self.ram = [0] * 0xFFFF
        for i, byte in enumerate(source):
            self.ram[i] = byte

        # cycle counter
        self.tick = 0

        self.registers = {
            "A": Z80Register("A", "Accumulator"),
        	"B": Z80Register("B", "Accumulator"),
        	"D": Z80Register("D", "Accumulator"),
        	"H": Z80Register("H", "Accumulator"),
        	"C": Z80Register("C", "Carry flag"),
        	"Z": Z80Register("Z", "Zero flag"),
        	"S": Z80Register("S", "Sign flag"),
        	"N": Z80Register("N", "Add/Sub flag"),
        	"L": Z80Register("L", "flag"),
        	"P/V": Z80Register("P/V", "Parity/overflow flag"),
        	"H": Z80Register("H", "Half carry flag"),
        	"IX": Z80Register("IX", "Index register"),
        	"IY": Z80Register("IY", "Index register"),
        	"I": Z80Register("I", "Interrupt vector"),
        	"R": Z80Register("R", "Memory refresh"),
        	"SP": Z80Register("SP", "Stack pointer"),
        	"PC": Z80Register("PC", "Program counter")}

        self.opcode_handlers = {
                0b00111110: self.handler_ld_r8_n,       # ld a, n
                0b00100001: self.handler_ld_r16_n_n,    # ld hl, n, n
                0b00000001: self.handler_ld_r16_n_n,    # ld bc, n, n
                0b11000011: self.handler_jp_n_n,
                0b00000000: self.handler_nop}

    def setup_flags_and_pc(self):
        self.registers["PC"].value = 0
        self.registers["C"].value = False
        self.registers["Z"].value = False
        self.registers["S"].value = False
        self.registers["N"].value = False
        self.registers["P/V"].value = False

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

    def instr_ld(self, reg_name, value):
        self.registers[reg_name].value = value

    def instr_jp(self):
        lower = self.fetch()
        self.increment()
        upper = self.fetch()
        self.increment()
        self.registers["PC"].value = upper << 8 | lower

    def fetch(self):
        return self.source[self.registers["PC"].value]

    def exec(self):
        self.setup_flags_and_pc()

        while self.tick < 100:
            self.tick += 1
            opcode = self.ram[self.registers["PC"].value]
            self.increment_pc()
            self.opcode_handlers[opcode](opcode)

