def plugin_main(vm):
    import keyboard
    import string
    import time

    def getch():
        alph = list(string.ascii_lowercase)
        while True:
            for l in alph:
                if keyboard.is_pressed(l):
                    return l
            for n in range(10):
                if keyboard.is_pressed(str(n)):
                    return str(n)
    while True:
        char = ord(getch())

        print("Pressed key keycode:", char)
        vm.io_lock.acquire()
        vm.io[0xA] = char
        vm.io_lock.release()
