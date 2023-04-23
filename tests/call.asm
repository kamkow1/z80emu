  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym

main:
  ld sp, 0x1234

  ld a, 22
  cp 22
  call z, aba_aba
  ld bc, 45

aba_aba:
  nop
  nop
  ld hl, 57
  ret

