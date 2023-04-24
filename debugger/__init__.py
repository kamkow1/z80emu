from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import vm
import sys


class Debugger:
    def __init__(self, source, syms):
        self.syms = {}
        for line in syms.splitlines():
            tokens = line.split()
            self.syms[tokens[0]] = int(tokens[2].replace("$", ""), 16)

        self.source = source
        self.vm = vm.VM(source)
        self.vm_playing = False
        self.vm_suspended = False
        imgui.create_context()
        self.window = self.impl_glfw_init()
        self.impl = GlfwRenderer(self.window)

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()

            imgui.new_frame()
            self.frame_cmds()
            if self.vm_playing and not self.vm.halt:
                if not self.vm_suspended:
                    self.vm.step()

            gl.glClearColor(0.1, 0.1, 0.1, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

    def __del__(self):
        self.end_debugger()

    def end_debugger(self):
        self.impl.shutdown()
        glfw.terminate()

    def impl_glfw_init(self):
        w, h = 800, 600
        window_name = "z80emu"
        if not glfw.init():
            print("Error: failed to initialize OpenGL context")
            sys.exit(1)

        window = glfw.create_window(w, h, window_name, None, None)
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Error: failed to initialize the window")
            sys.exit(1)
        return window

    def window_menu_bar(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("Debugger"):
                clicked, selected = imgui.menu_item("Exit")
                if clicked:
                    self.end_debugger()
                    sys.exit(0)
                imgui.end_menu()

            btn_play_clicked = imgui.button("Run program")
            if btn_play_clicked:
                self.vm_playing = True

            btn_suspend_clicked = imgui.button("Suspend execution")
            if btn_suspend_clicked:
                self.vm_suspended = True

            btn_reset_clicked = imgui.button("Reset")
            if btn_reset_clicked:
                self.vm = vm.VM(self.source)
                self.vm_playing = False

            imgui.end_main_menu_bar()

    def registers_table(self):
        if imgui.begin("Registers View"):
            if imgui.begin_table("Registers", 2):
                for key, value in self.vm.registers.items():
                    imgui.table_next_row()
                    imgui.table_set_column_index(0)
                    imgui.text(f"Reg {key}")
                    imgui.table_set_column_index(1)
                    imgui.text(str(value.value))
                imgui.end_table()
            imgui.end()

    def vm_status(self):
        if imgui.begin_table("VM Status", 2):
            # CPU halted
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("CPU halted")
            imgui.table_set_column_index(1)
            imgui.text(str(self.vm.halt))

            # Opcode
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("Opcode")
            imgui.table_set_column_index(1)
            imgui.text(str(hex(self.vm.opcode))
                       if self.vm.opcode else "No opcode")

            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("Label")
            imgui.table_set_column_index(1)
            label = "No label"
            for key, val in self.syms.items():
                if val == self.vm.registers["PC"].value:
                    label = key
            imgui.text(label)

            # Byte
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("Byte")
            imgui.table_set_column_index(1)
            imgui.text(str(hex(self.vm.ram[self.vm.registers["PC"].value])))

            # Execution status
            imgui.table_next_row()
            imgui.table_set_column_index(0)
            imgui.text("Status")
            imgui.table_set_column_index(1)
            text = "VM Not Running"
            if self.vm_suspended:
                text = "VM Suspended"
            elif self.vm_playing:
                text = "VM Running"
            imgui.text(text)

            imgui.end_table()

    def frame_cmds(self):
        if imgui.begin("z80emu debugger"):
            self.vm_status()

            self.window_menu_bar()
            self.registers_table()
            imgui.end()
