# handler for `OUT (n), A`
# takes the value of A reg and outputs
# it to a port specififed by (n)
def handler_out_n_a(self, opcode):
    port = self.ram[self.registers["PC"].value]
    self.increment_pc()
    self.vm_lock.acquire()
    self.io[port] = self.registers["A"].value
    self.vm_lock.release()


# handler for `IN a, (n)`
# takes the value passed onto a port
# specified by (n) and puts it into the A register
def handler_in_a_n(self, opcode):
    port = self.ram[self.registers["PC"].value]
    self.increment_pc()
    self.vm_lock.acquire()
    self.registers["A"].value = self.io[port]
    print("in a = ", self.registers["A"].value)
    self.vm_lock.release()

