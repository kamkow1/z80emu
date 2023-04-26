class Z80Register:
    def __init__(self, short_name, desc):
        self.value = None
        self.short_name = short_name
        self.desc = desc


class VM:
    from ._nop import handler_nop
    from ._cp import handler_cp_n
    from ._halt import handler_halt
    from ._jp import (
        handler_jp_n_n,
        handler_jp_z_n_n,
        handler_jp_nz_n_n,
    )
    from ._jr import (
        handler_jr_d,
        handler_jr_z_d,
        handler_jr_nz_d,
        handler_jr_c_d,
        handler_jr_nc_d
    )
    from ._ld import (
        handler_ld_r8_n,
        handler_ld_r16_n_n
    )
    from ._stack import (
        handler_call_n_n,
        handler_call_z_n_n,
        handler_call_nz_n_n,
        handler_call_nc_n_n,
        handler_call_c_n_n,
        handler_call_po_n_n,
        handler_call_pe_n_n,
        handler_call_p_n_n,
        handler_call_m_n_n,
        handler_ret,
        handler_push_r16,
        handler_pop_r16
    )
    from ._vmutils import dump_registers

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
        self.opcode = None
        self.ram = [0] * 0xFFFF
        for i, byte in enumerate(source):
            self.ram[i] = byte

        # cycle counter
        self.tick = 0

        # halt
        self.halt = False

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

        self.registers["PC"].value = 0
        self.registers["C"].value = False
        self.registers["Z"].value = False
        self.registers["S"].value = False
        self.registers["N"].value = False
        self.registers["P/V"].value = False

        self.opcode_handlers = {
                # -- Ld --
                0x3E: self.handler_ld_r8_n,       # ld a, n
                0x21: self.handler_ld_r16_n_n,    # ld hl, n, n
                0x01: self.handler_ld_r16_n_n,    # ld bc, n, n
                0x31: self.handler_ld_r16_n_n,    # ld sp, n, n

                # -- Jp --
                0xC3: self.handler_jp_n_n,
                0xCA: self.handler_jp_z_n_n,
                0xC2: self.handler_jp_nz_n_n,

                # -- Jr --
                0x18: self.handler_jr_d,
                0x28: self.handler_jr_z_d,
                0x20: self.handler_jr_nz_d,
                0x38: self.handler_jr_c_d,
                0x30: self.handler_jr_nc_d,

                # -- Call --
                0xCD: self.handler_call_n_n,
                0xCC: self.handler_call_z_n_n,
                0xC4: self.handler_call_nz_n_n,
                0xD4: self.handler_call_nc_n_n,
                0xDC: self.handler_call_c_n_n,
                0xE4: self.handler_call_po_n_n,
                0xEC: self.handler_call_pe_n_n,
                0xF4: self.handler_call_p_n_n,
                0xFC: self.handler_call_m_n_n,

                # -- Ret --
                0xC9: self.handler_ret,

                # -- Push --
                0xC5: self.handler_push_r16,
                0xD5: self.handler_push_r16,
                0xE5: self.handler_push_r16,
                0xF5: self.handler_push_r16,

                # -- Pop --
                0xC1: self.handler_pop_r16,
                0xD1: self.handler_pop_r16,
                0xE1: self.handler_pop_r16,
                0xF1: self.handler_pop_r16,

                # -- Cp --
                0xFE: self.handler_cp_n,

                # -- Halt --
                0x76: self.handler_halt,
                
                # -- Nop --
                0x0: self.handler_nop}

    def increment_pc(self):
        self.registers["PC"].value += 1

    def step(self):
        self.tick += 1
        self.opcode = self.ram[self.registers["PC"].value]
        print(f"OPCODE: {hex(self.opcode)}")

        self.increment_pc()

        try:
            self.opcode_handlers[self.opcode](self.opcode)
        except KeyError:
            print(f"Error: encountered an unknown opcode `{hex(self.opcode)}`")

    def exec(self):
        while True:
            if not self.halt:
                self.step()
