def dump_registers(self, iter):
    print(f"REGISTER STATE (ITERATION {iter}):")
    print("-------------------------------------")
    for key, reg in self.registers.items():
        print(f"{key} = {reg.value}")
    print("-------------------------------------")

def unsig_to_sig(x):
    if x & 0x80 == 0x80:
        return x - 256
    else:
        return x