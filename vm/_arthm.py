def handler_inc_r16(self, opcode):
    reg = (opcode >> 4) & 3
    if reg == 3:
        self.registers["SP"].value += 1
    else:
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
    self.registers[reg].value += 1


def handler_add_a_r8(self, opcode):
    reg = opcode & 4
    reg = self.bin_to_str_regs[reg]

    value = self.registers[reg].value
    self.registers["A"].value += value

    a = self.registers["A"].value

    self.registers["S"].value = a < 0
    self.registers["Z"].value = a == 0


def handler_add_a_n(self, opcode):
    value = self.ram[self.registers["PC"].value]
    self.increment_pc()

    self.registers["A"].value += value

    a = self.registers["A"].value
    self.registers["S"].value = a < 0
    self.registers["Z"].value = a == 0


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
    self.registers["H"].value = result >> 8
    self.registers["L"].value = result & 0xFF


def handler_cpl(self, opcode):
    self.registers["A"].value = ~self.registers["A"].value
