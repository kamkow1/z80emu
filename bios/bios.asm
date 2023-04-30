  .cr Z80
  .tf bios.bin, BIN
  .lf bios.lst
  .in bios/bios_defs.asm

  .or bios_def_vb_print_char
bios_vb_print_char:
  ld (hl), a
  inc hl
  ret
