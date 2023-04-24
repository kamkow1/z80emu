def dump_registers(self, iter):
    print(f"REGISTER STATE (ITERATION {iter}):")
    print("-------------------------------------")
    for key, reg in self.registers.items():
        print(f"{key} = {reg.value}")
    print("-------------------------------------")
