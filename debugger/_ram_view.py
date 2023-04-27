import imgui

def ram_view(self):
    if imgui.begin("RAM View"):
        if imgui.begin_table("RAM Cells", 32):
            addr = 0x0
            # 255 x 257 = 0xffff
            for row in range(2048):
                imgui.table_next_row()
                for col in range(32):
                    imgui.table_set_column_index(col)
                    idx = 32 * row + col
                    if idx > len(self.vm.ram):
                        imgui.end_table()
                        imgui.end()
                        return

                    if idx == len(self.vm.ram):
                        idx -= 1

                    data = self.vm.ram[idx]
                    text = str(hex(data))
                    is_label = False
                    for key, val in self.syms.items():
                        if val == addr:
                            is_label = True
                            break

                    # data highlighting
                    style = ()
                    if addr == self.vm.registers["PC"].value:
                        style = (0xff, 0x00, 0x00)
                    else:
                        if data != 0 and not is_label:
                            style = (0xff, 0xff, 0x00)
                        elif data == 0 and is_label:
                            style = (0x00, 0xff, 0x00)
                        elif data != 0 and is_label:
                            style = (0xff, 0xA5, 0x00)
                        else:
                            style = (0xff, 0xff, 0xff)

                    imgui.push_style_color(imgui.COLOR_TEXT, *style)
                    imgui.text(text)
                    imgui.pop_style_color()

                    if imgui.is_item_hovered():
                        tooltip = str(hex(addr))
                        if is_label:
                            tooltip += f" [{key}]"
                        imgui.set_tooltip(tooltip)
                    addr += 1
            imgui.end_table()
        imgui.end()