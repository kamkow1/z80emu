class Z80Register:
    def __init__(self, short_name):
        self.value = None
        self.short_name = short_name


class VM:
    from ._video import (
        video_update,
        video_end
    )

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
        handler_ld_r16_n_n,
        handler_ld_hl_n,
        handler_ld_hl_r8,
        handler_ld_r8_hl,
        handler_ld_bc_a,
        handler_ld_de_a,
        handler_ld_n_n_hl,
        handler_ld_n_n_a
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

        # init ram
        self.ram = [0] * (0xFFFF + 1)
        for i, byte in enumerate(source):
            self.ram[i] = byte

        # load BIOS
        with open("bios.bin", "rb") as bios_f:
            bios = bios_f.read()
            print(bios)
            for i in range(0, 0xFE01 - 0xF906):
                if i >= len(bios):
                    break
                self.ram[0xF906 + i] = bios[i]

        # cycle counter
        self.tick = 0

        # halt
        self.halt = False

        self.registers = {
                "A": Z80Register("A"),
                "B": Z80Register("B"),
                "C": Z80Register("C"),
                "D": Z80Register("D"),
                "E": Z80Register("E"),
                "H": Z80Register("H"),
                "L": Z80Register("L"),
                "N": Z80Register("N"),
                "S": Z80Register("S"),
                "Z": Z80Register("Z"),
                "P/V": Z80Register("P/V"),
                "IX": Z80Register("IX"),
                "IY": Z80Register("IY"),
                "I": Z80Register("I"),
                "R": Z80Register("R"),
                "SP": Z80Register("SP"),
                "PC": Z80Register("PC")}

        self.registers["PC"].value = 0
        self.registers["C"].value = False
        self.registers["Z"].value = False
        self.registers["S"].value = False
        self.registers["N"].value = False
        self.registers["P/V"].value = False

        self.opcode_handlers = {
                # -- Ld --
                0x3E: self.handler_ld_r8_n,          # ld a, n
                0x06: self.handler_ld_r8_n,          # ld b, n
                0x0E: self.handler_ld_r8_n,          # ld c, n
                0x16: self.handler_ld_r8_n,          # ld d, n
                0x1e: self.handler_ld_r8_n,          # ld e, n
                0x26: self.handler_ld_r8_n,          # ld h, n
                0x2E: self.handler_ld_r8_n,          # ld l, n
                0x21: self.handler_ld_r16_n_n,       # ld hl, n, n
                0x01: self.handler_ld_r16_n_n,       # ld bc, n, n
                0x11: self.handler_ld_r16_n_n,       # ld de, n, n
                0x31: self.handler_ld_r16_n_n,       # ld sp, n, n
                0x36: self.handler_ld_hl_n,          # ld (hl), n
                0x77: self.handler_ld_hl_r8,         # ld (hl), a
                0x70: self.handler_ld_hl_r8,         # ld (hl), b
                0x71: self.handler_ld_hl_r8,         # ld (hl), c
                0x72: self.handler_ld_hl_r8,         # ld (hl), d
                0x73: self.handler_ld_hl_r8,         # ld (hl), e
                0x74: self.handler_ld_hl_r8,         # ld (hl), h
                0x75: self.handler_ld_hl_r8,         # ld (hl), l
                0x7E: self.handler_ld_r8_hl,         # ld a, (hl)
                0x46: self.handler_ld_r8_hl,         # ld b, (hl)
                0x4E: self.handler_ld_r8_hl,         # ld c, (hl)
                0x56: self.handler_ld_r8_hl,         # ld d, (hl)
                0x5E: self.handler_ld_r8_hl,         # ld e, (hl)
                0x66: self.handler_ld_r8_hl,         # ld h, (hl)
                0x6E: self.handler_ld_r8_hl,         # ld l, (hl)
                0x02: self.handler_ld_bc_a,          # ld (bc), a
                0x12: self.handler_ld_de_a,          # ld (de), a
                0x22: self.handler_ld_n_n_hl,        # ld (nn), hl
                0x32: self.handler_ld_n_n_a,         # ld (nn), a

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
        if self.registers["PC"].value >= len(self.ram):
            return False
        self.opcode = self.ram[self.registers["PC"].value]
        #print(f"opcode {hex(self.opcode)}")

        self.increment_pc()

        if self.opcode not in self.opcode_handlers:
            print(f"Error: encountered an unknown opcode `{hex(self.opcode)}`")
        else:
            self.opcode_handlers[self.opcode](self.opcode)

        return self.video_update()

    def run(self):
        _continue = True
        while _continue:
            if not self.halt:
                _continue = self.step()
        self.video_end()
