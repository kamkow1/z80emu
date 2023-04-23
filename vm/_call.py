def perform_call(self):
    push_addr_low = self.ram[self.registers["PC"].value]
    self.increment_pc()
    push_addr_high = self.ram[self.registers["PC"].value]
    self.increment_pc()

    push_addr = (push_addr_high << 8) | push_addr_low
    self.stack_push(push_addr)
    self.registers["PC"].value = push_addr


def call_if(self, cond):
    if cond:
        perform_call(self)
    else:
        self.increment_pc()


def handler_call_n_n(self, opcode):
    perform_call(self)


def handler_call_z_n_n(self, opcode):
    call_if(self, self.registers["Z"].value)


def handler_call_nz_n_n(self, opcode):
    call_if(self, not self.registers["Z"].value)


def handler_call_nc_n_n(self, opcode):
    call_if(self, not self.registers["C"].value)


def handler_call_c_n_n(self, opcode):
    call_if(self, self.registers["C"].value)


def handler_call_po_n_n(self, opcode):
    call_if(self, not self.registers["P/V"].value)


def handler_call_pe_n_n(self, opcode):
    call_if(self, self.registers["P/V"].value)


def handler_call_p_n_n(self, opcode):
    call_if(self, not self.registers["S"].value)


def handler_call_m_n_n(self, opcode):
    call_if(self, self.registers["S"].value)
