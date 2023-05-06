  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc
  .in tests/conversions.inc


main:
    ld sp, 1000
    ld hl, sys_vb_begin 

    ; counter: from ascii 0 - 1
    ld b, 0

loop:
    ld hl, sys_vb_begin 
    ; call sys_video_clear    

    ld a, 10
    inc b
    cp b
    jp z, end

    ; ld a, b

    call sys_print_char

    jp loop

end:
    halt

