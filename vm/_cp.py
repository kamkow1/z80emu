# generic helper for variations of the `CP` instruction
# subtracts `value` from A reg without modifying it
# then sets approperiate flags
def cp_helper(self, value=None):
    if value == None:
        value = self.ram[self.registers["PC"].value]
    a = self.registers["A"].value
    result = a - value

    # set flags
    self.flags["S"].value = bool((result >> 7) & 1)
    self.flags["Z"].value = result == 0
    self.flags["N"].value = True
    self.flags["P/V"].value = result > 0xFF


# wrapper for `CP n`
def handler_cp_n(self, opcode):
    cp_helper(self)

# handler for `CP r8`
def handler_cp_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]
    cp_helper(self, value=self.registers[reg].value)
