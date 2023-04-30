  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.asm

main:
    ld sp, 1000

    ld a, 'a' 
    ld hl, bios_def_vb_begin
    call bios_def_vb_print_char
    halt
    
