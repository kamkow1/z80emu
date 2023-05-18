def handler_out_n_a(self, opcode):
    port = self.ram[self.registers["PC"].value]
    self.increment_pc()

    self.io[port] = self.registers["A"].value


def handler_in_a_n(self, opcode):
    port = self.ram[self.registers["PC"].value]
    self.increment_pc()
    self.registers["A"].value = self.io[port]
