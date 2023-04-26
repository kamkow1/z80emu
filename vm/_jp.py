from ._vmutils import unsig_to_sig

def perform_jp(self):
    low_byte = self.ram[self.registers["PC"].value]
    self.increment_pc()
    high_byte = self.ram[self.registers["PC"].value]
    self.registers["PC"].value = (high_byte << 8) | low_byte

def perform_jr(self):
    offset = unsig_to_sig(self.ram[self.registers["PC"].value])
    self.registers["PC"].value += offset
    print(self.registers["PC"].value)
    print(self.ram[self.registers["PC"].value])


def jp_if(self, cond):
    if cond:
        perform_jp(self)
    else:
        self.increment_pc()

def jr_if(self, cond):
    if cond:
        perform_jr(self)
    else:
        self.increment_pc()

def handler_jp_n_n(self, opcode):
    perform_jp(self)


def handler_jp_nz_n_n(self, opcode):
    jp_if(self, not self.registers["Z"].value)


def handler_jp_z_n_n(self, opcode):
    jp_if(self, self.registers["Z"].value)

def handler_jr_d(self, opcode):
    perform_jr(self)

def handler_jr_z_d(self, opcode):
    jr_if(self, self.registers["Z"].value)

def handler_jr_nz_d(self, opcode):
    jr_if(self, not self.registers["Z"].value)

def handler_jr_c_d(self, opcode):
    jr_if(self, self.registers["C"].value)

def handler_jr_nc_d(self, opcode):
    jr_if(self, not self.registers["C"].value)