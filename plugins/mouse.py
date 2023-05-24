def plugin_main(vm):
    import sdl2.ext.mouse

    def io_write_mouse_util(_vm):

        # 0xE -> mouse x
        # 0xF -> mouse y

        _vm.vm_lock.acquire()
        _vm.io[0xE] = _vm.mouse[0] # x
        _vm.io[0xF] = _vm.mouse[1] # y
        _vm.vm_lock.release()

        print(
            f"x = {_vm.io[0xE]}",
            f"y = {_vm.io[0xF]}"
        )
    while True:
        # update mouse
        vm.mouse = sdl2.ext.mouse.mouse_coords()
        io_write_mouse_util(vm)

