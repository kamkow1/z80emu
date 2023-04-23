#!/usr/bin/env python3

import sys
import vm

if len(sys.argv) < 2:
    print("Error: please provide an input file.\n",
          "Hint: main.py <path-to-compiled-z80-asm>")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    vm = vm.VM(f.read())
    vm.exec()

