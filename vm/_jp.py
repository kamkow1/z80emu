from ._vmutils import unsig_to_sig

def perform_jp(self):
    low_byte = self.ram[self.registers["PC"].value]
    self.increment_pc()
    high_byte = self.ram[self.registers["PC"].value]
    self.registers["PC"].value = (high_byte << 8) | low_byte


def handler_jp_n_n(self, opcode):
    perform_jp(self)


def handler_jp_nz_n_n(self, opcode):
    if not self.registers["Z"].value:
        perform_jp(self)
    else:
        self.increment_pc()


def handler_jp_z_n_n(self, opcode):
    if self.registers["Z"].value:
        perform_jp(self)
    else:
        self.increment_pc()

def handler_jr_d(self, opcode):
    #self.increment_pc()
    #offset = self.registers["PC"].value
    offset = unsig_to_sig(self.ram[self.registers["PC"].value])
    print(offset)
    print(self.registers["PC"].value)
    self.registers["PC"].value += offset
    print(self.registers["PC"].value)
    print(self.ram[self.registers["PC"].value])