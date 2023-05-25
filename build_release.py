import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROGRAM = "z80emu"
MAIN = "./main.py"

one_file = "--onefile" if sys.argv[1] == "one_file" else ""
PYINSTALLER_OPTS = [MAIN, "--name", PROGRAM, one_file]
print("OPTIONS: ", PYINSTALLER_OPTS)

subprocess.run(["pyinstaller", *PYINSTALLER_OPTS])
