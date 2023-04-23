def handler_jp_n_n(self, opcode):
    low_byte = self.ram[self.registers["PC"].value]
    self.increment_pc()
    high_byte = self.ram[self.registers["PC"].value]
    self.registers["PC"].value = (high_byte << 8) | low_byte


def handler_jp_nz_n_n(self, opcode):
    if not self.registers["Z"].value:
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.registers["PC"].value = (high_byte << 8) | low_byte
    else:
        self.increment_pc()


def handler_jp_z_n_n(self, opcode):
    if self.registers["Z"].value:
        low_byte = self.ram[self.registers["PC"].value]
        self.increment_pc()
        high_byte = self.ram[self.registers["PC"].value]
        self.registers["PC"].value = (high_byte << 8) | low_byte
    else:
        self.increment_pc()
