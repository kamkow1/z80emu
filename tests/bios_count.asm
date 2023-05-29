  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc


main:
    ld sp, 1000
    ld hl, sys_vb_begin 

    ; counter: from ascii 0 - 1
    ld b, 0x30

loop:
    ld a, 0x3A
    inc b
    cp b
    jp z, end

    ld a, b
    call sys_print_char
	inc hl
	ld a, 0xA
	call sys_print_char
	inc hl

    jp loop

end:
	ld hl, sys_vb_begin
	call sys_video_clear
	jp main

