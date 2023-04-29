import sys


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

    if reg == 0:
        self.registers["B"].value = high_byte
        self.registers["C"].value = low_byte
    elif reg == 1:
        self.registers["D"].value = high_byte
        self.registers["E"].value = low_byte
    elif reg == 2:
        self.registers["H"].value = high_byte
        self.registers["L"].value = low_byte
    elif reg == 3:
        self.registers["SP"].value = (high_byte << 8) | low_byte
    else:
        print("Error: unhandled register in handler_ld_r16_n_n():",
              f"`{hex(reg)}`")
        sys.exit(1)


def ld_indirect_addr_helper(self, pair, value, inc_pc):
    if inc_pc:
        self.increment_pc()

    low_byte = self.registers[pair[1]].value
    high_byte = self.registers[pair[0]].value

    full_addr = high_byte << 8 | low_byte
    self.ram[full_addr] = value


def ld_from_indirect_addr_into_r8_helper(self, opcode, pair):
    reg = (opcode & 56) >> 3
    low_byte = self.registers[pair[1]].value
    high_byte = self.registers[pair[0]].value

    full_addr = high_byte << 8 | low_byte
    data = self.ram[full_addr]
    self.registers[self.bin_to_str_regs[reg]].value = data


def handler_ld_hl_n(self, opcode):
    data = self.ram[self.registers["PC"].value]
    ld_indirect_addr_helper(self, "HL", data, inc_pc=True)


def handler_ld_hl_r8(self, opcode):
    reg = ((opcode << 5) & (7 << 9)) >> 9
    data = self.registers[self.bin_to_str_regs[reg]].value
    ld_indirect_addr_helper(self, "HL", data, inc_pc=False)


def handler_ld_r8_hl(self, opcode):
    ld_from_indirect_addr_into_r8_helper(self, opcode, "HL")


def handler_ld_n_n_hl(self, opcode):
    n_low = self.ram[self.registers["PC"].value]
    self.increment_pc()
    n_high = self.ram[self.registers["PC"].value]
    self.increment_pc()
    full_addr = n_high << 8 | n_low

    h = self.registers["H"].value
    l = self.registers["L"].value
    hl = h << 8 | l

    self.ram[full_addr] = hl


def handler_ld_n_n_a(self, opcode):
    n_low = self.ram[self.registers["PC"].value]
    self.increment_pc()
    n_high = self.ram[self.registers["PC"].value]
    self.increment_pc()
    full_addr = n_high << 8 | n_low
    self.ram[full_addr] = self.registers["A"].value


def handler_ld_bc_a(self, opcode):
    data = self.registers["A"].value
    ld_indirect_addr_helper(self, "BC", data, inc_pc=False)


def handler_ld_de_a(self, opcode):
    data = self.registers["A"].value
    ld_indirect_addr_helper(self, "DE", data, inc_pc=False)
