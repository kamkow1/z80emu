  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym

main:
  ld a, 33
  cp 33
  jr z, 6
  ld hl, 22
  ld bc, 33
  nop
  ld hl, 69
  ld bc, 22
  halt