# helper function for performing `JP ...` insutrctions
# arg value is loaded up from ram as the next byte
# the `PC` reg is set to the arg, making the VM
# change it's execution point
def perform_jp(self):
    low_byte = self.ram[self.registers["PC"].value]
    self.increment_pc()
    high_byte = self.ram[self.registers["PC"].value]
    self.registers["PC"].value = (high_byte << 8) | low_byte


# wrapper for conditional jumps
def jp_if(self, cond):
    if cond:
        perform_jp(self)
    else:
        self.increment_pc()
        self.increment_pc()


# handler for `JP nn`
def handler_jp_n_n(self, opcode):
    perform_jp(self)


# handler for `JP nz, nn`
# jumps if the `Z` flag is unset
def handler_jp_nz_n_n(self, opcode):
    jp_if(self, not self.flags["Z"].value)


# handler for `JP z, nn`
# jumps if the `Z` flag is set
def handler_jp_z_n_n(self, opcode):
    jp_if(self, self.flags["Z"].value)
