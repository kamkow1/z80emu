import sys
from threading import Thread, Lock


class Z80Register:
    def __init__(self, short_name, width, init_value):
        self.short_name = short_name
        self.value = init_value
        self.width = width


class Z80FlagBit:
    def __init__(self, short_name, desc):
        self.short_name = short_name
        self.value = False
        self.desc = desc


class VM:
    from ._video import (
        video_update,
        video_end
    )

    from ._nop import handler_nop
    from ._halt import handler_halt
    from ._io import (
        handler_out_n_a,
        handler_in_a_n
    )
    from ._cp import (
        handler_cp_n,
        handler_cp_r8
    )
    from ._arthm import (
        handler_inc_r16,
        handler_inc_r8,
        handler_add_a_r8,
        handler_add_a_n,
        handler_add_hl_r16,
        handler_cpl,
        handler_sbc_a_r8,
        handler_sub_r8,
        handler_and_r8,
        handler_or_r8
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
    from ._vmutils import (
        dump_registers,
        compose_F_register,
    )

    bin_to_str_regs = {
            0b111: "A",
            0b000: "B",
            0b001: "C",
            0b010: "D",
            0b011: "E",
            0b100: "H",
            0b101: "L"}

    def __init__(self, source, plugins):
        self.source = source
        self.opcode = None

        # init ram
        self.ram = [0] * (0xFFFF + 1)
        for i, byte in enumerate(source):
            self.ram[i] = byte

        # init io
        self.io = [0] * 0x100
        # protect self.io so it can be shared between plugin theads
        self.io_lock = Lock()

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

        # Xn is an unused flag bit for backwards compatilbility purposes
        self.flags = {
                "S": Z80FlagBit("S", "Sign flag. Set when the result of an operation was negative"),
                "Z": Z80FlagBit("Z", "Zero flag. Set when an operation results in 0"),
                "X1": Z80FlagBit("X", ""),
                "N": Z80FlagBit("N", "Addition / Subtration flag. Set when the previous instruction was `SUB`"),
                "X1": Z80FlagBit("X", ""),
                "P/V": Z80FlagBit("P/V", "Parity / Overflow flag. Set when a number overflows"),
                "CY": Z80FlagBit("CY", "Carry flag. Set depending whether an operation caused a carry or a borrow")}

        # some registers (eg. index registers) were left off
        # because the VM doesn't support the instructions
        # which would require those registers to be implemented
        self.registers = {
                "A": Z80Register("A", 8, 0),
                "B": Z80Register("B", 8, 0),
                "C": Z80Register("C", 8, 0),
                "D": Z80Register("D", 8, 0),
                "E": Z80Register("E", 8, 0),
                "F": Z80Register("F", 8, 0),
                "H": Z80Register("H", 8, 0),
                "L": Z80Register("L", 8, 0),
                "SP": Z80Register("SP", 16, 0),
                "PC": Z80Register("PC", 16, 0)}

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
                0x7F: self.handler_ld_r8_r8,         # ld a, a
                0x78: self.handler_ld_r8_r8,         # ld a, b
                0x79: self.handler_ld_r8_r8,         # ld a, c
                0x7A: self.handler_ld_r8_r8,         # ld a, d
                0x7B: self.handler_ld_r8_r8,         # ld a, e
                0x7C: self.handler_ld_r8_r8,         # ld a, h
                0x7D: self.handler_ld_r8_r8,         # ld a, l
                0x47: self.handler_ld_r8_r8,         # ld b, a
                0x40: self.handler_ld_r8_r8,         # ld b, b
                0x41: self.handler_ld_r8_r8,         # ld b, c
                0x42: self.handler_ld_r8_r8,         # ld b, d
                0x43: self.handler_ld_r8_r8,         # ld b, e
                0x44: self.handler_ld_r8_r8,         # ld b, h
                0x45: self.handler_ld_r8_r8,         # ld b, l
                0x4F: self.handler_ld_r8_r8,         # ld c, a
                0x48: self.handler_ld_r8_r8,         # ld c, b
                0x49: self.handler_ld_r8_r8,         # ld c, c
                0x4A: self.handler_ld_r8_r8,         # ld c, d
                0x4B: self.handler_ld_r8_r8,         # ld c, e
                0x4C: self.handler_ld_r8_r8,         # ld c, h
                0x4D: self.handler_ld_r8_r8,         # ld c, l
                0x57: self.handler_ld_r8_r8,         # ld d, a
                0x50: self.handler_ld_r8_r8,         # ld d, b
                0x51: self.handler_ld_r8_r8,         # ld d, c
                0x52: self.handler_ld_r8_r8,         # ld d, d
                0x53: self.handler_ld_r8_r8,         # ld d, e
                0x54: self.handler_ld_r8_r8,         # ld d, h
                0x55: self.handler_ld_r8_r8,         # ld d, l
                0x5F: self.handler_ld_r8_r8,         # ld e, a
                0x58: self.handler_ld_r8_r8,         # ld e, b
                0x59: self.handler_ld_r8_r8,         # ld e, c
                0x5A: self.handler_ld_r8_r8,         # ld e, d
                0x5B: self.handler_ld_r8_r8,         # ld e, e
                0x5C: self.handler_ld_r8_r8,         # ld e, h
                0x5D: self.handler_ld_r8_r8,         # ld e, l
                0x67: self.handler_ld_r8_r8,         # ld h, a
                0x60: self.handler_ld_r8_r8,         # ld h, b
                0x61: self.handler_ld_r8_r8,         # ld h, c
                0x62: self.handler_ld_r8_r8,         # ld h, d
                0x63: self.handler_ld_r8_r8,         # ld h, e
                0x64: self.handler_ld_r8_r8,         # ld h, h
                0x65: self.handler_ld_r8_r8,         # ld h, l
                0x6F: self.handler_ld_r8_r8,         # ld l, a
                0x68: self.handler_ld_r8_r8,         # ld l, b
                0x69: self.handler_ld_r8_r8,         # ld l, c
                0x6A: self.handler_ld_r8_r8,         # ld l, d
                0x6B: self.handler_ld_r8_r8,         # ld l, e
                0x6C: self.handler_ld_r8_r8,         # ld l, h
                0x6D: self.handler_ld_r8_r8,         # ld l, l

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

                # -- Add --
                0xC6: self.handler_add_a_n,           # add a, n
                0x87: self.handler_add_a_r8,          # add a, a
                0x80: self.handler_add_a_r8,          # add a, b
                0x81: self.handler_add_a_r8,          # add a, c
                0x82: self.handler_add_a_r8,          # add a, d
                0x83: self.handler_add_a_r8,          # add a, e
                0x84: self.handler_add_a_r8,          # add a, h
                0x85: self.handler_add_a_r8,          # add a, l
                0x09: self.handler_add_hl_r16,        # add hl, bc
                0x19: self.handler_add_hl_r16,        # add hl, de
                0x29: self.handler_add_hl_r16,        # add hl, hl
                0x39: self.handler_add_hl_r16,        # add hl, sp
                
                # -- Sub --
                0x97: self.handler_sub_r8,            # sub a
                0x90: self.handler_sub_r8,            # sub b
                0x91: self.handler_sub_r8,            # sub c
                0x92: self.handler_sub_r8,            # sub d
                0x93: self.handler_sub_r8,            # sub e
                0x94: self.handler_sub_r8,            # sub h
                0x95: self.handler_sub_r8,            # sub l

                # -- Sbc --
                0x9F: self.handler_sbc_a_r8,          # sbc a, a
                0x98: self.handler_sbc_a_r8,          # sbc a, b
                0x99: self.handler_sbc_a_r8,          # sbc a, c
                0x9A: self.handler_sbc_a_r8,          # sbc a, d
                0x9B: self.handler_sbc_a_r8,          # sbc a, e
                0x9C: self.handler_sbc_a_r8,          # sbc a, h
                0x9D: self.handler_sbc_a_r8,          # sbc a, l

                0xA7: self.handler_and_r8,            # and a
                0xA0: self.handler_and_r8,            # and b
                0xA1: self.handler_and_r8,            # and c
                0xA2: self.handler_and_r8,            # and d
                0xA3: self.handler_and_r8,            # and e
                0xA4: self.handler_and_r8,            # and h
                0xA5: self.handler_and_r8,            # and l

                0xB7: self.handler_or_r8,             # or a
                0xB0: self.handler_or_r8,             # or b
                0xB1: self.handler_or_r8,             # or c
                0xB2: self.handler_or_r8,             # or d
                0xB3: self.handler_or_r8,             # or e
                0xB4: self.handler_or_r8,             # or h
                0xB5: self.handler_or_r8,             # or l

                # -- Cpl --
                0x2F: self.handler_cpl,               # cpl

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

                # -- Io --
                0xD3: self.handler_out_n_a,          # out (n), a
                0xDB: self.handler_in_a_n,           # in a, (n)

                # -- Halt --
                0x76: self.handler_halt,            # halt

                # -- Nop --
                0x0: self.handler_nop}              # nop

        # Run plugins
        self.plugin_threads = []
        for plugin in plugins:
            plugin_f = plugin[0]
        with open(plugin_f, "r") as f:
            plugin_cnts = f.read()
            lcs = locals()
            exec(plugin_cnts, globals(), lcs)
            # assume the user provided this function
            plugin_main = lcs["plugin_main"]
            plugin_thread = Thread(
                target=plugin_main,
                args=(self,)
            )
            plugin_thread.start()
            self.plugin_threads.append(plugin_thread)

    def join_plugin_threads(self):
        print("aaaa")
        for pth in self.plugin_threads:
            pth.join()

    def end_vm(self):
        self.join_plugin_threads()

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
            sys.exit(1)
        else:
            #print(f"opcode {hex(self.opcode)}")
            self.opcode_handlers[self.opcode](self.opcode)
            self.compose_F_register()

        return self.video_update()

    def run(self):
        _continue = True
        while _continue:
            if not self.halt:
                _continue = self.step()
        self.video_end()
