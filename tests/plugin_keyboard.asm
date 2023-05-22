  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

_main:
  ld hl, sys_vb_begin
  jp main

main:
  ld sp, 1000

  in a, (0xA)
  call sys_print_char
  jp main
