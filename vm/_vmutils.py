def dump_registers(self, iter):
    print(f"REGISTER STATE (ITERATION {iter}):")
    print("-------------------------------------")
    for key, reg in self.registers.items():
        print(f"{key} = {reg.value}")
    print("-------------------------------------")

def unsig_to_sig(x):
    return x - 256 if x & 0x80 == 0x80 else x


def sig_to_unsig(x):
    return x & 0xFFFF
