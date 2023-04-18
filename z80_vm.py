import sys


class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


class VM:
    def __init__(self):
        self.registers = {}
        self.registers["A"] = Z80Register("A", "Accumulator")
        self.registers["B"] = Z80Register("B", "Accumulator")
        self.registers["D"] = Z80Register("D", "Accumulator")
        self.registers["H"] = Z80Register("H", "Accumulator")
        self.registers["C"] = Z80Register("C", "Flag")
        self.registers["F"] = Z80Register("F", "Flag")
        self.registers["E"] = Z80Register("E", "Flag")
        self.registers["L"] = Z80Register("L", "Flag")
        self.registers["IX"] = Z80Register("IX", "Index register")
        self.registers["IY"] = Z80Register("IY", "Index register")
        self.registers["I"] = Z80Register("I", "Interrupt vector")
        self.registers["R"] = Z80Register("R", "Memory refresh")
        self.registers["SP"] = Z80Register("SP", "Stack pointer")
        self.registers["PC"] = Z80Register("PC", "Program counter")

    def exec(self, instrs):
        print("TODO: VM.exec()")
        sys.exit(1)

