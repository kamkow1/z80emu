  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym

main:
  ld (hl), 56
  halt

