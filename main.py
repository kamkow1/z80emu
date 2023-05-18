#!/usr/bin/env python3

import sys
import argparse
import vm
import debugger


parser = argparse.ArgumentParser(description="a z80 chip emulator")
parser.add_argument("file")
parser.add_argument("-debug", action="store_true")
parser.add_argument("-sym", type=str, nargs="?")
parser.add_argument("-plugin", type=str, nargs="*", action="append")
args = parser.parse_args()

with open(sys.argv[1], "rb") as f:
    source = f.read()
    if args.debug:
        dbg = debugger.Debugger(
            source=source,
            sym_path=args.sym,
            render_syms=args.sym is not None,
            vm_plugins=args.plugin
        )
        dbg.end_debugger()
    else:
        v = vm.VM(source, args.plugin)
        v.run()
        v.end_vm()
