import sys


def stack_push(self, value):
    self.registers["SP"].value -= 1
    self.ram[self.registers["SP"].value] = value


def stack_pop(self):
    self.registers["SP"].value += 1
    return self.ram[self.registers["SP"].value]


def call_helper(self):
    # get args
    addr_low = self.ram[self.registers["PC"].value]
    self.increment_pc()
    addr_high = self.ram[self.registers["PC"].value]
    self.increment_pc()

    self.registers["SP"].value -= 1
    pc_high = self.registers["PC"].value >> 8
    self.ram[self.registers["SP"].value] = pc_high

    self.registers["SP"].value -= 1
    pc_low = self.registers["PC"].value & 0xFF
    self.ram[self.registers["SP"].value] = pc_low

    addr = (addr_high << 8) | addr_low
    self.registers["PC"].value = addr


def ret_helper(self):
    ret_addr_low = self.ram[self.registers["SP"].value]
    self.registers["SP"].value += 1
    ret_addr_high = self.ram[self.registers["SP"].value]
    self.registers["SP"].value += 1

    ret_addr = ret_addr_high << 8 | ret_addr_low

    self.registers["PC"].value = ret_addr


def push_regpair_helper(self, reg1, reg2):
    stack_push(self, self.registers[reg1].value)
    stack_push(self, self.registers[reg2].value)


def pop_regpair_helper(self, reg1, reg2):
    self.registers[reg2].value = stack_pop(self)
    self.registers[reg1].value = stack_pop(self)


def handler_push_r16(self, opcode):
    reg = (opcode >> 4) & 3
    if reg == 0:
        push_regpair_helper(self, "B", "C")
    elif reg ==1:
        push_regpair_helper(self, "D", "E")
    elif reg == 2:
        push_regpair_helper(self, "H", "L")
    elif reg == 3:
        push_regpair_helper(self, "A", "F")
    else:
        print("Error: unhandled register in handler_push_r16():",
              f"`{hex(reg)}`")
        sys.exit(1)


def handler_pop_r16(self, opcode):
    reg = (opcode >> 4) & 3
    if reg == 0:
        pop_regpair_helper(self, "B", "C")
    elif reg == 1:
        pop_regpair_helper(self, "D", "E")
    elif reg == 2:
        pop_regpair_helper(self, "H", "L")
    elif reg == 3:
        pop_regpair_helper(self, "A", "F")
    else:
        print("Error: unhandled register in handler_pop_r16():",
              f"`{hex(reg)}`")
        sys.exit(1)


def call_if(self, cond):
    if cond:
        call_helper(self)
    else:
        self.increment_pc()


def handler_call_n_n(self, opcode):
    call_helper(self)


def handler_call_z_n_n(self, opcode):
    call_if(self, self.flags["Z"].value)


def handler_call_nz_n_n(self, opcode):
    call_if(self, not self.flags["Z"].value)


def handler_call_nc_n_n(self, opcode):
    call_if(self, not self.flags["CY"].value)


def handler_call_c_n_n(self, opcode):
    call_if(self, self.flags["CY"].value)


def handler_call_po_n_n(self, opcode):
    call_if(self, not self.flags["P/V"].value)


def handler_call_pe_n_n(self, opcode):
    call_if(self, self.flags["P/V"].value)


def handler_call_p_n_n(self, opcode):
    call_if(self, not self.flags["S"].value)


def handler_call_m_n_n(self, opcode):
    call_if(self, self.flags["S"].value)


def handler_ret(self, opcode):
    ret_helper(self)


def handler_ret_z(self, opcode):
    if self.flags["Z"].value:
        ret_helper(self)


def handler_ret_nz(self, opcode):
    if not self.flags["Z"].value:
        ret_helper(self)


def handler_ret_c(self, opcode):
    if self.flags["CY"].value:
        ret_helper(self)

def handler_ret_nc(self, opcode):
    if not self.flags["CY"].value:
        ret_helper(self)


def handler_ret_pe(self, opcode):
    if self.flags["P/V"].value:
        ret_helper(self)


def handler_ret_po(self, opcode):
    if not self.flags["P/V"].value:
        ret_helper(self)


def handler_ret_m(self, opcode):
    if self.flags["S"].value:
        ret_helper(self)


def handler_ret_p(self, opcode):
    if not self.flags["S"].value:
        ret_helper(self)
