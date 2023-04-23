def setup_flags_and_pc(self):
    self.registers["PC"].value = 0
    self.registers["C"].value = False
    self.registers["Z"].value = False
    self.registers["S"].value = False
    self.registers["N"].value = False
    self.registers["P/V"].value = False


def dump_registers(self, iter):
    print(f"REGISTER STATE (ITERATION {iter}):")
    print("-------------------------------------")
    for key, reg in self.registers.items():
        print(f"{key} = {reg.value}")
    print("-------------------------------------")
