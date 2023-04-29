def perform_jp(self):
    low_byte = self.ram[self.registers["PC"].value]
    self.increment_pc()
    high_byte = self.ram[self.registers["PC"].value]
    self.registers["PC"].value = (high_byte << 8) | low_byte


def jp_if(self, cond):
    if cond:
        perform_jp(self)
    else:
        self.increment_pc()


def handler_jp_n_n(self, opcode):
    perform_jp(self)


def handler_jp_nz_n_n(self, opcode):
    jp_if(self, not self.registers["Z"].value)


def handler_jp_z_n_n(self, opcode):
    jp_if(self, self.registers["Z"].value)
