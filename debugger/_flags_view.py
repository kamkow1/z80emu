import imgui

def flags_view(self):
    if imgui.begin("Flags View"):
        if imgui.begin_table("Flags", 2):
            for key, value in self.vm.flags.items():
                # skip unused flags
                if key[0] == "X":
                    continue

                imgui.table_next_row()
                imgui.table_set_column_index(0)
                imgui.text(f"Flag {key}")
                imgui.table_set_column_index(1)
                imgui.text(str(value.value))
            imgui.end_table()
        imgui.end()
