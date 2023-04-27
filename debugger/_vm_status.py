import imgui

def vm_status(self):
    halt = str(self.vm.halt)
    opcode = str(hex(self.vm.opcode)) if self.vm.opcode else "No opcode"
    label = "No label"
    for key, val in self.syms.items():
        if val == self.vm.registers["PC"].value:
            label = key
    byte = str(hex(self.vm.ram[self.vm.registers["PC"].value]))
    status = "VM Not Running"
    if self.vm_suspended:
        status = "VM Suspended"
    elif self.vm_playing:
        status = "VM Running"
    time = str(self.time)

    if imgui.begin_table("VM Status", 2):
        # CPU halted
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("CPU halted")
        imgui.table_set_column_index(1)
        imgui.text(halt)

        # Opcode
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("Opcode")
        imgui.table_set_column_index(1)
        imgui.text(opcode)

        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("Label")
        imgui.table_set_column_index(1)
        imgui.text(label)

        # Byte
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("Byte")
        imgui.table_set_column_index(1)
        imgui.text(byte)

        # Execution status
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("Status")
        imgui.table_set_column_index(1)
        imgui.text(status)

        # Time
        imgui.table_next_row()
        imgui.table_set_column_index(0)
        imgui.text("Time")
        imgui.table_set_column_index(1)
        imgui.text(time)

        imgui.end_table()

        text_val = "z80emu_status_dump.json"
        changed, filename = imgui.input_text("", text_val)
        json_str = "{"
        if imgui.button("Save"):
            print("-- Saving to file --")
            json_str += f"\"halt\": {halt.lower()},"
            json_str += f"\"opcode\": \"{opcode}\","
            json_str += f"\"label\": \"{label}\","
            json_str += f"\"byte\": {int(byte, 16)},"
            json_str += f"\"status\": \"{status}\","
            json_str += f"\"time\": {time}"
            json_str += "}"

            import os
            dirent = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(dirent, filename), "w") as f:
                f.write(json_str)