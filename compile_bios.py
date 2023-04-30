#!/usr/bin/env python

import sys
import os
import subprocess

SBASM = "sbasm.py"
BIOS = os.path.join(
    os.path.dirname(__file__),
    "bios",
    "bios.asm")

if len(sys.argv) > 1:
    # sbasm path was provided
    SBASM = sys.argv[1]

subprocess.run([SBASM, BIOS])

