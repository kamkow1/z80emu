  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym

; video = 0xFE01
video = 0xFE00
bios_vb_print_char = 0xF906

main:
    ld sp, 1000

    ld a, 'a' 
    ld hl, video
    call bios_vb_print_char
    halt
    
