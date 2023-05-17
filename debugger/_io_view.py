import imgui

def io_view(self):
    if imgui.begin("IO View"):
        if imgui.begin_table("IO View", 16):
            port = 0
            for row in range(16):
                imgui.table_next_row()
                for col in range(16):
                    imgui.table_set_column_index(col)
                    imgui.text(str(hex(self.vm.io[port])))

                    if imgui.is_item_hovered():
                        imgui.set_tooltip(str(hex(port)))
                    port += 1

            imgui.end_table()
    imgui.end()
