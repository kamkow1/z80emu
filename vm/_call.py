def handler_call_n_n(self, opcode):
    push_addr_low = self.ram[self.registers["PC"].value]
    self.increment_pc()
    push_addr_high = self.ram[self.registers["PC"].value]
    self.increment_pc()

    push_addr = (push_addr_high << 8) | push_addr_low
    self.stack_push(push_addr)
    self.registers["PC"].value = push_addr
