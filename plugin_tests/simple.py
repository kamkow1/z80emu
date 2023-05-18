
def plugin_main(vm):
    import time
    print("yay called plugin_main()")

    while True:
        vm.io_lock.acquire()
        print(vm.io[0x10])
        vm.io_lock.release()
        time.sleep(0.1)
