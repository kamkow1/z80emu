class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


class VM:
    from ._nop import handler_nop
    from ._jp import handler_jp_n_n, handler_jp_z_n_n, handler_jp_nz_n_n
    from ._ld import handler_ld_r8_n, handler_ld_r16_n_n
    from ._cp import handler_cp_n
    from ._call import handler_call_n_n
    from ._ret import handler_ret
    from ._stack_helpers import stack_pop, stack_push
    from ._vmutils import dump_registers, setup_flags_and_pc

    bin_to_str_regs = {
            0b111: "A",
            0b000: "B",
            0b001: "C",
            0b010: "D",
            0b011: "E",
            0b100: "H",
            0b101: "L"}

    def __init__(self, source):
        self.source = source
        self.ram = [0] * 0xFFFF
        for i, byte in enumerate(source):
            self.ram[i] = byte

        # cycle counter
        self.tick = 0

        self.registers = {
                "A": Z80Register("A", "Accumulator"),
                "B": Z80Register("B", "Accumulator"),
                "D": Z80Register("D", "Accumulator"),
                "H": Z80Register("H", "Accumulator"),
                "C": Z80Register("C", "Carry flag"),
                "Z": Z80Register("Z", "Zero flag"),
                "S": Z80Register("S", "Sign flag"),
                "N": Z80Register("N", "Add/Sub flag"),
                "L": Z80Register("L", "flag"),
                "P/V": Z80Register("P/V", "Parity/overflow flag"),
                "IX": Z80Register("IX", "Index register"),
                "IY": Z80Register("IY", "Index register"),
                "I": Z80Register("I", "Interrupt vector"),
                "R": Z80Register("R", "Memory refresh"),
                "SP": Z80Register("SP", "Stack pointer"),
                "PC": Z80Register("PC", "Program counter")}

        self.opcode_handlers = {
                0x3E: self.handler_ld_r8_n,       # ld a, n
                0x21: self.handler_ld_r16_n_n,    # ld hl, n, n
                0x01: self.handler_ld_r16_n_n,    # ld bc, n, n
                0x31: self.handler_ld_r16_n_n,    # ld sp, n, n
                0xC3: self.handler_jp_n_n,
                0xCA: self.handler_jp_z_n_n,
                0xC2: self.handler_jp_nz_n_n,
                0xFE: self.handler_cp_n,
                0xCD: self.handler_call_n_n,
                0xC9: self.handler_ret,
                0x00: self.handler_nop}

    def increment_pc(self):
        self.registers["PC"].value += 1

    def exec(self):
        self.setup_flags_and_pc()

        while self.tick < len(self.source):
            self.tick += 1
            opcode = self.ram[self.registers["PC"].value]
            print(f"OPCODE: {hex(opcode)}")
            self.increment_pc()
            try:
                self.opcode_handlers[opcode](opcode)
            except KeyError:
                print(f"Error: encountered an unknown opcode `{hex(opcode)}`")
