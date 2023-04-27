import imgui


class Breakpoint:
    def __init__(self, instr, addr, on_state):
        self.instr = instr
        self.addr = addr
        self.on_state = on_state


def breakpoints_view(self):
    if imgui.begin("Break points"):
        if imgui.begin_table("Break points", 3):
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("BP")
            imgui.table_set_column_index(1)
            imgui.text("at")
            imgui.table_set_column_index(2)
            imgui.text("on/off")

            for i, bp in enumerate(self.breakpoints):
                imgui.table_next_row()
                imgui.table_set_column_index(0)
                imgui.text(f"{hex(bp.instr)}")
                imgui.table_set_column_index(1)
                imgui.text(f"{hex(bp.addr)}")
                imgui.table_set_column_index(2)
                imgui.text(f"{'ON' if bp.on_state else 'OFF'}")
            imgui.end_table()

            imgui.push_id("addr")
            addr = 0x0
            changed1, addr = imgui.input_text("", str(hex(addr)))
            imgui.pop_id()

            imgui.push_id("on_state")
            on_state = True
            changed2, on_state = imgui.input_text("", str(on_state))
            imgui.pop_id()

            if imgui.button("Add BP"):
                addr = int(addr, 16)
                on_state = bool(on_state)
                instr = self.vm.ram[addr]
                self.breakpoints.append(Breakpoint(instr, addr + 3, on_state))
        imgui.end()
