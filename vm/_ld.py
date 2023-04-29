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


def ld_indirect_addr_helper(self, pair, inc_pc):
    data = self.ram[self.registers["PC"].value]
    if inc_pc:
        self.increment_pc()

    low_byte = self.registers[pair[1]].value
    high_byte = self.registers[pair[0]].value

    full_addr = high_byte << 8 | low_byte
    self.ram[full_addr] = data


def handler_ld_hl_n_indirect(self, opcode):
    ld_indirect_addr_helper(self, "HL", inc_pc=True)
