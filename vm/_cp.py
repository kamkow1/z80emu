def handler_cp_n(self, opcode):
    a = self.registers["A"].value
    # result = (a & 0xFF) - (self.ram[self.registers["PC"].value] & 0xFF)
    #print("result = ", result)
    result = a - self.ram[self.registers["PC"].value]
    self.registers["Z"].value = result == 0
    self.increment_pc()
