from ._vmutils import (
    calc_carry8,
    calc_carry16
)


# increments a 16 bit register pair
# SP is handled as a special case,
# since it doesn't divide into lower and upper bits
def handler_inc_r16(self, opcode):
    reg = (opcode >> 4) & 3
    # hanlde SP
    if reg == 3:
        self.registers["SP"].value += 1
        return 
    rh = None
    rl = None
    # Pick the right register pair
    if reg == 0:
        rh = (self.registers["B"].value, "B")
        rl = (self.registers["C"].value, "C")
    elif reg == 1:
        rh = (self.registers["D"].value, "D")
        rl = (self.registers["E"].value, "E")
    elif reg == 2:
        rh = (self.registers["H"].value, "H")
        rl = (self.registers["L"].value, "L")

    # decompose registers and save
    full = rh[0] << 8 | rl[0]
    full += 1
    low = full & 0xFF
    high = full >> 8
    self.registers[rh[1]].value = high
    self.registers[rl[1]].value = low


# increments a single 8 bit register
def handler_inc_r8(self, opcode):
    reg = (opcode >> 3) & 7
    reg = self.bin_to_str_regs[reg]

    old_val = self.registers[reg].value
    self.registers[reg].value += 1
    val = self.registers[reg].value

    # set flags
    # TODO: set H flag
    self.flags["S"].value = val < 0
    self.flags["Z"].value = val == 0
    self.flags["N"].value = False
    self.flags["P/V"].value = old_val == 0x7F


# adds an 8 bit register to the A register
def handler_add_a_r8(self, opcode):
    reg = opcode & 7
    reg = self.bin_to_str_regs[reg]

    value = self.registers[reg].value
    new_a = self.registers["A"].value + value
    self.registers["A"].value = new_a & 0xFF

    a = self.registers["A"].value

    # set flags
    self.flags["S"].value = a < 0
    self.flags["Z"].value = a == 0
    self.flags["CY"].value = calc_carry8(new_a)


# adds some value `n` to register A
def handler_add_a_n(self, opcode):
    value = self.ram[self.registers["PC"].value]
    self.increment_pc()

    #self.registers["A"].value += value
    new_a = self.registers["A"].value + value
    self.registers["A"].value = new_a & 0xFF

    # set flags
    a = self.registers["A"].value
    self.flags["S"].value = a < 0
    self.flags["Z"].value = a == 0
    self.flags["CY"].value = new_a > 0xFF


# adds a 16 bit register pair to HL register pair
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
    self.flags["N"].value = False
    self.flags["CY"].value = calc_carry16(result)


# inverts the bits of A register
def handler_cpl(self, opcode):
    self.registers["A"].value = -1 * self.registers["A"].value - 1


# subtracts an8 bit register from A
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


# subtracts an 8 bit register from A,
# but takes the carry flag into consideration
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

# performs a logical and on A
def handler_and_r8(self, opcode):
    reg = opcode & 7
    reg = self.registers[reg].value
    value = self.registers["A"].value & reg
    self.registers["A"].value = value

    # set flags
    # NOTE: skip half-carry flag
    self.flags["CY"].value = False
    self.flags["N"].value = False
    self.flags["P/V"].value = value > 0xFF
    self.flags["Z"].value = value == 0
    self.flags["S"].value = value < 0


# performs logical or on A
def handler_or_r8(self, opcode):
    reg = opcode & 7
    reg = self.registers[reg].value
    value = self.registers["A"].value | reg
    self.registers["A"].value = value

    # set flags
    # NOTE: skip hald-carry flag
    self.flags["CY"].value = False
    self.flags["N"].value = False
    self.flags["P/V"].value = value > 0xFF
    self.flags["Z"].value = value == 0
    self.flags["S"].value = value < 0
