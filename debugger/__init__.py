from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui
import vm
from ._breakpoints_view import Breakpoint
import sys
from timeit import default_timer


class Debugger:
    from ._ram_view import ram_view
    from ._window_menu_bar import window_menu_bar
    from ._registers_view import registers_view
    from ._vm_status import vm_status
    from ._breakpoints_view import breakpoints_view
    from ._flags_view import flags_view
    from ._io_view import io_view

    def __init__(self, source, sym_path, render_syms, vm_plugins):
        self.render_syms = render_syms
        self.syms = {}

        if self.render_syms:
            with open(sym_path, "r") as f:
                string = f.read()
                for line in string.splitlines():
                    tokens = line.split()
                    if len(tokens) < 3:
                        continue
                    self.syms[tokens[0]] = int(tokens[2].replace("$", ""), 16)

        self.source = source
        self.vm = vm.VM(source, vm_plugins)
        self.breakpoints = []
        self.vm_playing = False
        self.vm_suspended = False
        self.timer_start = 0.0
        self.time = 0.0
        imgui.create_context()
        self.window = self.impl_glfw_init()
        self.impl = GlfwRenderer(self.window)

        imgui.get_io().ini_file_name = None

        # break on the first instruction
        self.breakpoints.append(Breakpoint(
            self.vm.ram[self.vm.registers["PC"].value],
            self.vm.registers["PC"].value))

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()

            imgui.new_frame()
            self.frame_cmds()
            if self.vm_playing and not self.vm.halt:
                _break = False
                pc = self.vm.registers["PC"].value
                for bp in self.breakpoints:
                    _break = pc == bp.addr

                if not self.vm_suspended and not _break:
                    self.vm.step()

            gl.glClearColor(0.1, 0.1, 0.1, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

    def end_debugger(self):
        self.impl.shutdown()
        glfw.terminate()
        self.vm.video_end()
        self.vm.end_vm()

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

    def frame_cmds(self):
        if self.vm_playing and not self.vm_suspended:
            self.time = default_timer() - self.timer_start

        if imgui.begin("z80emu debugger"):
            self.window_menu_bar()
            self.vm_status()
            self.registers_view()
            self.flags_view()
            self.io_view()
            self.ram_view()
            self.breakpoints_view()
            imgui.end()
