from ._vmutils import unsig_to_sig  

def perform_jr(self):
    offset = unsig_to_sig(self.ram[self.registers["PC"].value])
    self.registers["PC"].value += offset
    print(self.registers["PC"].value)
    print(self.ram[self.registers["PC"].value])

def jr_if(self, cond):
    if cond:
        perform_jr(self)
    else:
        self.increment_pc()

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