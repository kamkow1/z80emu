# z80emu

z80emu is an emulator of the famous Z80 chip by Zilog.
This project was made for educational purposes, so there are likely a lot of bugs etc.

# Development Goals

- [x] (Done partially) Implement the core instruction set from [this site](https://clrhome.org/table)
- [x] (vm/_video.py) Emulate video
- [x] (debugger/) Debug mode that displays registers, memory and allows to step through instructions
- [x] Open architecture. [read more](https://en.wikipedia.org/wiki/Open_architecture)

# Supported instructions
The project most likely won't support all Z80 instructions.
If you'd like to know which instructions this emulator supports specifically,
see the file `__init__.py` in `vm/`. In the `VM` class constructor there are
all the implemented instructions listed.

# Resources

- [instructions](https://clrhome.org/table)
- [z80 wiki](https://wikiti.brandonw.net/?title=Z80_Instruction_Set)
- [z80 history](https://mitsi.com/2021/12/21/a-bit-of-z80-history/)

# How to run

For both Linux and Windows you will need sbasm. you can get it [from here](https://www.sbprojects.net/sbasm/).
Now you are able to compile some test programs

# Setup

```bash
# Create Virtualenv
python3 -m venv venv

# Activate the Virtualenv
source venv/bin/activate # For Linux
venv/Scripts/Activate.ps1 # For Windows (Powershell)
venv/Scripts/Activate.bat # For Windows (Cmd)

# Install dependecies
pip install -r requirements.txt
```

# Compiling BIOS

```bash
./compile_bios.py
# or
python3 ./compile_bios.py 
```

Note that the `compile_bios.py` script assumes that the sbasm path is just `sbasm.py`.
if you have sbasm in a different directory, then invoke `compile_bios.py` like:

```bash
./compile_bios.py path/to/directory/with/sbasm.py
```

This will result in `bios.bin` and `bios.lst`. We don't care about `bios.lst`.
`bios.bin` is loaded up into RAM by the emulator.

## Run

```bash
# will yield `out.bin`, `out.lst`, `out.sym`
python3 path/to/sbasm.py tests/bios_print_loader.asm

python3 main.py out.bin # will just run the emulator

# `out.sym` is required if you'd like to see some useful info about labels
python3 main.py out.bin -debug -sym out.sym
```

# Architecture

## Memory

<img src="https://raw.githubusercontent.com/kamkow1/z80emu/master/assets/Memory_Diagram.png" />
