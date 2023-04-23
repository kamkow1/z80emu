import sys


class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


class VM:
    bin_to_str_regs = {
            0b111: "A",
            0b000: "B",
            0b001: "C",
            0b010: "D",
            0b011: "E",
            0b100: "H",
            0b101: "L"}

    def __init__(self, source):
        self.source = source
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
                "IX": Z80Register("IX", "Index register"),
                "IY": Z80Register("IY", "Index register"),
                "I": Z80Register("I", "Interrupt vector"),
                "R": Z80Register("R", "Memory refresh"),
                "SP": Z80Register("SP", "Stack pointer"),
                "PC": Z80Register("PC", "Program counter")}

        self.opcode_handlers = {
                0x3E: self.handler_ld_r8_n,       # ld a, n
                0x21: self.handler_ld_r16_n_n,    # ld hl, n, n
                0x01: self.handler_ld_r16_n_n,    # ld bc, n, n
                0x31: self.handler_ld_r16_n_n,    # ld sp, n, n
                0xC3: self.handler_jp_n_n,
                0xCA: self.hanlder_jp_z_n_n,
                0xC2: self.hanlder_jp_nz_n_n,
                0xFE: self.handler_cp_n,
                0xCD: self.handler_call_n_n,
                0xC9: self.handler_ret,
                0x00: self.handler_nop}

    def increment_pc(self):
        self.registers["PC"].value += 1

    def handler_nop(self, opcode):
        pass

    def handler_jp_n_n(self, opcode):
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.registers["PC"].value = (high_byte << 8) | low_byte

    def hanlder_jp_nz_n_n(self, opcode):
        if not self.registers["Z"].value:
            low_byte = self.ram[self.registers["PC"].value]
            self.increment_pc()
            high_byte = self.ram[self.registers["PC"].value]
            self.registers["PC"].value = (high_byte << 8) | low_byte
        else:
            self.increment_pc()

    def hanlder_jp_z_n_n(self, opcode):
        if self.registers["Z"].value:
            low_byte = self.ram[self.registers["PC"].value]
            self.increment_pc()
            high_byte = self.ram[self.registers["PC"].value]
            self.registers["PC"].value = (high_byte << 8) | low_byte
        else:
            self.increment_pc()

    def handler_cp_n(self, opcode):
        a = self.registers["A"].value
        self.increment_pc()
        result = a - self.ram[self.registers["PC"].value]
        print(result)

        if a == result:
            self.registers["Z"].value = True
        else:
            self.registers["Z"].value = False

        if a < result:
            if result >= 0:
                # unsigned
                self.registers["C"].value = True
            else:
                # signed
                if self.registers["S"].value == self.registers["P/V"]:
                    self.registers["S"].value = True

    def handler_ld_r8_n(self, opcode):
        reg = (opcode >> 3) & 7
        if reg not in self.bin_to_str_regs:
            print(f"Error: encoutnered an unknown register `{hex(reg)}`")
            sys.exit(1)

        data = self.ram[self.registers["PC"].value]
        self.increment_pc()
        self.registers[self.bin_to_str_regs[reg]].value = data

    def handler_ld_r16_n_n(self, opcode):
        reg = (opcode >> 4) & 3
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()

        if reg == 0x0:
            # BC
            self.registers["B"].value = high_byte
            self.registers["C"].value = low_byte
        elif reg == 0x2:
            # HL
            self.registers["H"].value = high_byte
            self.registers["L"].value = low_byte
        elif reg == 0x3:
            self.registers["SP"].value = (high_byte << 8) | low_byte
        else:
            print("Error: unhandled register in handler_ld_r16_n_n():",
                  f"`{hex(reg)}`")
            sys.exit(1)

    def handler_call_n_n(self, opcode):
        push_addr_low = self.ram[self.registers["PC"].value]
        self.increment_pc()
        push_addr_high = self.ram[self.registers["PC"].value]
        self.increment_pc()

        push_addr = (push_addr_high << 8) | push_addr_low
        self.stack_push(push_addr)
        self.registers["PC"].value = push_addr

    def handler_ret(self, opcode):
        self.registers["PC"].value = self.stack_pop()

    def stack_push(self, value):
        self.ram[self.registers["SP"].value] = value
        self.registers["SP"].value -= 1

    def stack_pop(self):
        self.registers["SP"].value += 1
        return self.ram[self.registers["SP"].value]

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

    def exec(self):
        self.setup_flags_and_pc()

        while self.tick < len(self.source):
            self.tick += 1
            opcode = self.ram[self.registers["PC"].value]
            print(f"OPCODE: {hex(opcode)}")
            self.increment_pc()
            try:
                self.opcode_handlers[opcode](opcode)
            except KeyError:
                print(f"Error: encountered an unknown opcode `{hex(opcode)}`")
