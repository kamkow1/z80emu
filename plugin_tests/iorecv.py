def plugin_main(vm):
    while True:
        vm.vm_lock.acquire()
        vm.io[0xA] = ord("K")
        vm.io[0xB] = ord("A")
        vm.io[0xC] = ord("M")
        vm.io[0xD] = ord("I")
        vm.io[0xE] = ord("L")
        vm.io[0xF] = ord("!")
        vm.vm_lock.release()
