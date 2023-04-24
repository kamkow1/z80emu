#!/usr/bin/env python3

import sys
import argparse
import vm
import debugger


parser = argparse.ArgumentParser(description="a z80 chip emulator")
parser.add_argument("file")
parser.add_argument("-debug", action="store_true")
args = parser.parse_args()

with open(sys.argv[1], "rb") as f:
    source = f.read()
    if args.debug:
        dbg = debugger.Debugger(source)
    else:
        vm.VM(source).exec()
