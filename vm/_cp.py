def handler_cp_n(self, opcode):
    a = self.registers["A"].value
    self.increment_pc()
    result = a - self.ram[self.registers["PC"].value]

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
