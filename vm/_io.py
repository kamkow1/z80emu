def handler_out_n_a(self, opcode):
    port = self.ram[self.registers["PC"].value]
    self.increment_pc()

    self.io[port] = self.registers["A"].value
