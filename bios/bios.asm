  .cr Z80
  .tf bios.bin, BIN
  .lf bios.lst
  .in bios/bios_defs.inc
  .or sys_bios_begin 

; bios jump table
; must begin at `sys_bios_begin`
  .db 0xC3
  .dw impl_sys_print_char

  .db 0xC3
  .dw impl_sys_print_str

  .db 0xC3
  .dw impl_sys_print_foo


impl_sys_print_char:
  ld (hl), a
  inc hl
  ret

impl_sys_print_str:
  ld a, (bc)

  ; check if null
  cp 0
  ret nz

  call impl_sys_print_char 
  inc bc
  jp impl_sys_print_str
