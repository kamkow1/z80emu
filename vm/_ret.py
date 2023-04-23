def handler_ret(self, opcode):
    self.registers["PC"].value = self.stack_pop()
