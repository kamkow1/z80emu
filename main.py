#!/usr/bin/env python3

import sys
import argparse
import vm
import debugger


parser = argparse.ArgumentParser(description="a z80 chip emulator")
parser.add_argument("file")
parser.add_argument("-debug", action="store_true")
parser.add_argument("-sym", type=str, nargs="?")
args = parser.parse_args()

with open(sys.argv[1], "rb") as f:
    source = f.read()
    if args.debug:
        with open(args.sym, "r") as syms:
            dbg = debugger.Debugger(source, syms.read())
            dbg.end_debugger()
    else:
        vm.VM(source).run()
