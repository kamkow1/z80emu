import imgui
import sys
from timeit import default_timer
import vm


def window_menu_bar(self):
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("Debugger"):
            clicked, selected = imgui.menu_item("Exit")
            if clicked:
                self.end_debugger()
                sys.exit(0)
            imgui.end_menu()

        if imgui.button("Run"):
            self.timer_start = default_timer()
            self.vm_playing = True
            self.vm_suspended = False

        if imgui.button("Suspend"):
            self.vm_suspended = True

        if imgui.button("Reset"):
            self.vm = vm.VM(self.source, self.vm.plugins)
            self.vm_playing = False

        if imgui.button("Next BP"):
            self.breakpoints.pop(0)

        imgui.end_main_menu_bar()
