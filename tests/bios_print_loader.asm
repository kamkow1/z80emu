  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

_main:
    jp main

main:
    ld sp, 1000

    ld hl, sys_vb_begin 
    ld b, 0
    jp progbar_loop

frame_loop:
    ; new frame
    ld b, 0
    call sys_video_clear
    ld hl, sys_vb_begin 

progbar_loop:
    ld a, '>'
    call sys_print_char

    ld a, 32
    inc b
    cp b
    jp z, frame_loop

    jp progbar_loop

end:
    halt
