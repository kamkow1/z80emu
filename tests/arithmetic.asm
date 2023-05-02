  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

main:
  ld b, 34
  ld a, 35
  add a, b
  add a, 351
