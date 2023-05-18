  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

main:
  ld a, 1
  out (0x10), a
  ld a, 2
  out (0x10), a
  ld a, 4
  out (0x10), a
  ld a, 8
  out (0x10), a
  ld a, 16
  out (0x10), a
  ld a, 32
  out (0x10), a
  ld a, 64
  out (0x10), a
  ld a, 128
  out (0x10), a

  jp main
