  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.asm

_main:
  jp main

haha:
    .az "ich liebe kasprzak und roman is ein bester Lehrer"

main:
    ld sp, 1000
    ld hl, sys_vb_begin 

    ld bc, haha
    call sys_print_str

    halt
    
