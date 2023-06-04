  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

_main:
  ld hl, sys_vb_begin
  ld sp, 1000
  jp main
 
x10:   .az "x = 100"

loadx:
  ld bc, x10 
  ret

main:

  in a, (0xE)
  ld b, 100 
  cp b
  call z, loadx

  call sys_print_str
  ld a, 0xA ; \n
  call sys_print_char

  jp main
