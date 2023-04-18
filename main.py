#!/usr/bin/env python3

import sys
import z80_parser
import z80_vm

if len(sys.argv) < 2:
    print("Error: please provide an input file.\n",
          "Hint: main.py <path-to-compiled-z80-asm>")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    instrs = z80_parser.parse(f.read())
    vm = z80_vm.VM()
    vm.exec(instrs)

