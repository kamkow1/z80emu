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
