import imgui

def registers_view(self):
    if imgui.begin("Registers View"):
        if imgui.begin_table("Registers", 3):
            for key, value in self.vm.registers.items():
                imgui.table_next_row()

                imgui.table_set_column_index(0)
                imgui.text(f"Reg {key}")

                imgui.table_set_column_index(1)
                imgui.text(str(value.value))

                imgui.table_set_column_index(2)
                fmt = "0" + str(value.width) + "b"
                imgui.text(format(value.value, fmt))
            imgui.end_table()
        imgui.end()
