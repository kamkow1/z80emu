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


def compose_F_register(self):
    binstr = ""
    for fname, fvalue in self.flags.items():
        if fname[0] == "X":
            # unused bit
            continue
        binstr += str(int(fvalue.value))
    self.registers["F"].value = int(binstr, 2)


def calc_carry8(value):
    if value <= 0xFF:
        return False
    return (value >> 7) & 1


def calc_carry16(value):
    if value <= 0xFFFF:
        return False
    return (value >> 15) & 1
