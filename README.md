# z80emu

z80emu is an emulator of the famous Z80 chip by Zilog.
This project was made for educational purposes, so there are likely a lot of bugs etc.

# Development Goals

- [ ] Implement the core instruction set from [this site](https://clrhome.org/table)
- [x] Emulate video
- [x] Debug mode that displays registers, memory and allows to step through instructions
- [ ] Open architecture. [read more](https://en.wikipedia.org/wiki/Open_architecture)

# Supported instructions
The project most likely won't support all Z80 instructions.
If you'd like to know which instructions this emulator supports specifically,
see the file `__init__.py` in `vm/`. In the `VM` class constructor there are
all the implemented instructions listed.

# Resources

- [instructions](https://clrhome.org/table)
- [z80 wiki](https://wikiti.brandonw.net/?title=Z80_Instruction_Set)
- [z80 history](https://mitsi.com/2021/12/21/a-bit-of-z80-history/)
