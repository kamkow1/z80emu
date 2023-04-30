
def handler_inc_hl(self, opcode):
    h = self.registers["H"].value
    l = self.registers["L"].value
    hl = h << 8 | l
    hl += 1

    low = hl & 0xFF
    high = hl >> 8
    self.registers["H"].value = high
    self.registers["L"].value = low
