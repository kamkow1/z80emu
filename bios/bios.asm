  .cr Z80
  .tf bios.bin, BIN
  ; start from 0xFF00 - 1530
  .or 0xF906

; params:
;   - a = character to print
bios_vb_print_char:
  ld (hl), a
  ret
