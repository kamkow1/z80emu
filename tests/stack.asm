  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym


main:
  ld sp, 0x1234
  call some_label

some_other_label:
  nop
  nop
  ld bc, 2233

some_label:
  nop
  nop
  ld hl, 23
  ret
