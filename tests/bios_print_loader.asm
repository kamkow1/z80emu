  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

_main:
    jp main

info:
    .az "printing a progress bar"

main:
    ld sp, 1000
    ld hl, sys_vb_begin 

    ; init counter
    ld d, 0

    ld bc, info
    call sys_print_str
    ld a, 0xA ; \n
    call sys_print_char

loop:

    ld a, '-'
    call sys_print_char

    ; assert c < 32
    ld a, 32
    inc d
    cp d
    jp z, end

    jp loop

end:
    halt
