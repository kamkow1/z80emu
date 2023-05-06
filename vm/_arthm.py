from carryutils import (
    calc_carry8,
    calc_carry16
)


def handler_inc_r16(self, opcode):
    reg = (opcode >> 4) & 3
    if reg == 3:
        self.registers["SP"].value += 1
        return 
    rh = None
    rl = None
    if reg == 0:
        rh = (self.registers["B"].value, "B")
        rl = (self.registers["C"].value, "C")
    elif reg == 1:
        rh = (self.registers["D"].value, "D")
        rl = (self.registers["E"].value, "E")
    elif reg == 2:
        rh = (self.registers["H"].value, "H")
        rl = (self.registers["L"].value, "L")
    full = rh[0] << 8 | rl[0]
    full += 1
    low = full & 0xFF
    high = full >> 8
    self.registers[rh[1]].value = high
    self.registers[rl[1]].value = low


def handler_inc_r8(self, opcode):
    reg = (opcode >> 3) & 7
    reg = self.bin_to_str_regs[reg]

    old_val = self.registers[reg].value
    self.registers[reg].value += 1
    val = self.registers[reg].value

    # set flags
    # TODO: set H flag
    self.registers["S"].value = val < 0
    self.registers["Z"].value = val == 0
    self.registers["N"].value = False
    self.registers["P/V"].value = old_val == 0x7F


def handler_add_a_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]

    value = self.registers[reg].value
    new_a = self.registers["A"].value + value
    self.registers["A"].value = new_a & 0xFF

    a = self.registers["A"].value

    # set flags
    self.registers["S"].value = a < 0
    self.registers["Z"].value = a == 0
    self.registers["C"].value = calc_carry8(new_a)


def handler_add_a_n(self, opcode):
    value = self.ram[self.registers["PC"].value]
    self.increment_pc()

    #self.registers["A"].value += value
    new_a = self.registers["A"].value + value
    self.registers["A"].value = new_a & 0xFF

    # set flags
    a = self.registers["A"].value
    self.registers["S"].value = a < 0
    self.registers["Z"].value = a == 0
    self.registers["C"].value = new_a > 0xFF


def handler_add_hl_r16(self, opcode):
    regpair = (opcode >> 4) & 3
    h = self.registers["H"].value
    l = self.registers["L"].value
    hl = h << 8 | l

    if regpair == 3:
        regpair = self.registers["SP"].value
    else:
        if regpair == 0:
            regpair = "BC"
        elif regpair == 1:
            regpair = "DE"
        elif regpair == 2:
            regpair = "HL"

        rh = self.registers[regpair[0]].value
        rl = self.registers[regpair[1]].value
        regpair = rh << 8 | rl

    result = hl + regpair
    masked_result = result & 0xFFFF
    self.registers["H"].value = masked_result >> 8
    self.registers["L"].value = masked_result & 0xFF

    # set flags
    self.registers["N"].value = False
    self.registers["C"].value = calc_carry16(result)


def handler_cpl(self, opcode):
    self.registers["A"].value = ~self.registers["A"].value


def handler_sub_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]

    value = self.registers[reg].value
    new_a = self.registers["A"].value - value
    self.registers["A"].value = new_a & 0xFF

    # set flags
    self.flags["S"].value = new_a < 0
    self.flags["Z"].value = new_a == 0
    self.flags["CY"].value = new_a < 0


def handler_sbc_a_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]

    value = self.registers[reg].value
    new_a = self.registers["A"].value - value

    if self.flags["CY"].value:
        new_a -= 1

    self.registers["A"].value = new_a & 0xFF

    # set flags
    self.flags["S"].value = new_a < 0
    self.flags["Z"].value = new_a == 0
