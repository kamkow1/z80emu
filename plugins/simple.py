
def plugin_main(vm):
    import time
    print("yay called plugin_main()")

    while True:
        vm.vm_lock.acquire()
        print(vm.io[0x10])
        vm.vm_lock.release()
        time.sleep(0.1)
