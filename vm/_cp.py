from ._vmutils import sig_to_unsig


def cp_helper(self, value=None):
    if value == None:
        value = self.ram[self.registers["PC"].value]
    a = self.registers["A"].value
    result = a - value

    # set flags
    self.registers["S"].value = (result >> 7) & 1
    self.registers["Z"].value = result == 0
    self.registers["N"].value = True
    self.registers["P/V"].value = result > 0xFF
    # self.registers["C"].value = sig_to_unsig(a) - sig_to_unsig(value) > 0xFF



def handler_cp_n(self, opcode):
    cp_helper(self)


def handler_cp_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]
    cp_helper(self, value=self.registers[reg].value)
