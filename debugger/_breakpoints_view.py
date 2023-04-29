import imgui


class Breakpoint:
    def __init__(self, instr, addr):
        self.instr = instr
        self.addr = addr


def breakpoints_view(self):
    if imgui.begin("Break points"):
        if imgui.begin_table("Break points", 3):
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("Instruction")
            imgui.table_set_column_index(1)
            imgui.text("Address")

            for i, bp in enumerate(self.breakpoints):
                imgui.table_next_row()
                imgui.table_set_column_index(0)
                imgui.text(f"{hex(bp.instr)}")
                imgui.table_set_column_index(1)
                imgui.text(f"{hex(bp.addr)}")
            imgui.end_table()

            addr = 0x0
            done, new_addr = imgui.input_text("", "", flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
            if done:
                addr = int(new_addr, 16)
                instr = self.vm.ram[addr]
                self.breakpoints.append(Breakpoint(instr, addr))
        imgui.end()
