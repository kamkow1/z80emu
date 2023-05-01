class Z80Register:
    def __init__(self, short_name, init_value):
        self.short_name = short_name
        self.value = init_value


class VM:
    from ._video import (
        video_update,
        video_end
    )

    from ._nop import handler_nop
    from ._halt import handler_halt
    from ._cp import (
        handler_cp_n,
        handler_cp_r8
    )
    from ._arthm import (
        handler_inc_r16,
        handler_inc_r8
    )
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
        handler_ld_bc_a,
        handler_ld_de_a,
        handler_ld_n_n_hl,
        handler_ld_n_n_a,
        handler_ld_a_from_hl_ptr,
        handler_ld_a_from_bc_ptr,
        handler_ld_a_from_de_ptr,
        handler_ld_r8_r8
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
        handler_ret_z,
        handler_ret_nz,
        handler_ret_c,
        handler_ret_nc,
        handler_ret_po,
        handler_ret_pe,
        handler_ret_p,
        handler_ret_m,
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
            for i in range(0, 0xFE00 - 0xFA00):
                if i >= len(bios):
                    break
                self.ram[0xFA00 + i] = bios[i]

        # cycle counter
        self.tick = 0

        # halt
        self.halt = False

        self.registers = {
                "A": Z80Register("A", 0),
                "B": Z80Register("B", 0),
                "C": Z80Register("C", 0),
                "D": Z80Register("D", 0),
                "E": Z80Register("E", 0),
                "H": Z80Register("H", 0),
                "L": Z80Register("L", 0),
                "N": Z80Register("N", 0),
                "S": Z80Register("S", 0),
                "Z": Z80Register("Z", 0),
                "P/V": Z80Register("P/V", 0),
                "IX": Z80Register("IX", 0),
                "IY": Z80Register("IY", 0),
                "I": Z80Register("I", 0),
                "R": Z80Register("R", 0),
                "SP": Z80Register("SP", 0),
                "PC": Z80Register("PC", 0)}


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
                0x7E: self.handler_ld_a_from_hl_ptr, # ld a, (hl)
                0x0A: self.handler_ld_a_from_bc_ptr, # ld a, (bc)
                0x1A: self.handler_ld_a_from_de_ptr, # ld a, (de)
                0x02: self.handler_ld_bc_a,          # ld (bc), a
                0x12: self.handler_ld_de_a,          # ld (de), a
                0x22: self.handler_ld_n_n_hl,        # ld (nn), hl
                0x32: self.handler_ld_n_n_a,         # ld (nn), a
                0x7B: self.handler_ld_r8_r8,         # ld a, e

                # -- Inc --
                0x23: self.handler_inc_r16,           # inc hl
                0x03: self.handler_inc_r16,           # inc bc
                0x13: self.handler_inc_r16,           # inc de
                0x33: self.handler_inc_r16,           # inc sp
                0x3C: self.handler_inc_r8,            # inc a
                0x04: self.handler_inc_r8,            # inc b
                0x0C: self.handler_inc_r8,            # inc c
                0x14: self.handler_inc_r8,            # inc d
                0x1C: self.handler_inc_r8,            # inc e
                0x24: self.handler_inc_r8,            # inc h
                0x2C: self.handler_inc_r8,            # inc l

                # -- Jp --
                0xC3: self.handler_jp_n_n,           # jp n, n
                0xCA: self.handler_jp_z_n_n,         # jp z, n, n
                0xC2: self.handler_jp_nz_n_n,        # jp nz, n, n

                # -- Jr --
                0x18: self.handler_jr_d,             # jr d
                0x28: self.handler_jr_z_d,           # jr z, d
                0x20: self.handler_jr_nz_d,          # jr nz, d
                0x38: self.handler_jr_c_d,           # jr c, d
                0x30: self.handler_jr_nc_d,          # jr nc, d

                # -- Call --
                0xCD: self.handler_call_n_n,         # call n, n
                0xCC: self.handler_call_z_n_n,       # call z, n, n
                0xC4: self.handler_call_nz_n_n,      # call nz, n, n
                0xD4: self.handler_call_nc_n_n,      # call nc, n, n
                0xDC: self.handler_call_c_n_n,       # call c, n, n
                0xE4: self.handler_call_po_n_n,      # call po, n, n
                0xEC: self.handler_call_pe_n_n,      # call pe, n, n
                0xF4: self.handler_call_p_n_n,       # call p, n, n
                0xFC: self.handler_call_m_n_n,       # call m, n, n

                # -- Ret --
                0xC9: self.handler_ret,              # ret
                0xC8: self.handler_ret_z,            # ret z
                0xC0: self.handler_ret_nz,           # ret nz
                0xE0: self.handler_ret_po,           # ret po
                0xE8: self.handler_ret_pe,           # ret pe
                0xD8: self.handler_ret_c,            # ret c
                0xD0: self.handler_ret_nc,           # ret nc
                0xF0: self.handler_ret_p,            # ret p
                0xF8: self.handler_ret_m,            # ret m

                # -- Push --
                0xC5: self.handler_push_r16,         # push bc
                0xD5: self.handler_push_r16,         # push de
                0xE5: self.handler_push_r16,         # push hl
                0xF5: self.handler_push_r16,         # push af

                # -- Pop --
                0xC1: self.handler_pop_r16,          # pop bc
                0xD1: self.handler_pop_r16,          # pop de
                0xE1: self.handler_pop_r16,          # pop hl
                0xF1: self.handler_pop_r16,          # pop af

                # -- Cp --
                0xFE: self.handler_cp_n,             # cp n
                0xBF: self.handler_cp_r8,            # cp a
                0xB8: self.handler_cp_r8,            # cp b
                0xB9: self.handler_cp_r8,            # cp c
                0xBA: self.handler_cp_r8,            # cp d
                0xBB: self.handler_cp_r8,            # cp e
                0xBC: self.handler_cp_r8,            # cp h
                0xBD: self.handler_cp_r8,            # cp l

                # -- Halt --
                0x76: self.handler_halt,            # halt

                # -- Nop --
                0x0: self.handler_nop}              # nop

    def increment_pc(self):
        self.registers["PC"].value += 1

    def step(self):
        self.tick += 1
        if self.registers["PC"].value >= len(self.ram):
            return False
        self.opcode = self.ram[self.registers["PC"].value]

        self.increment_pc()

        if self.opcode not in self.opcode_handlers:
            print(f"Error: encountered an unknown opcode `{hex(self.opcode)}`")
        else:
            print(f"opcode {hex(self.opcode)}")
            self.opcode_handlers[self.opcode](self.opcode)

        return self.video_update()

    def run(self):
        _continue = True
        while _continue:
            if not self.halt:
                _continue = self.step()
        self.video_end()
