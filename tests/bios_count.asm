  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc


num_to_hl_point:
  ld a, (hl)
  
num_to_a:
  ld h, 0
  ld l, a

num_to_hl:
  ld bc, -10000
  call one
  ld bc, -1000
  call one
  ld bc, -100
  call one
  ld bc, -10
  call one
  ld c, -1
one:
  ld a, '0'-1
two:
  inc a
  add hl, bc
  jr c, two
  push bc
  push af
  ld a, b
  cpl
  ld b, a
  ld a, c
  cpl
  ld c, a
  inc bc
  call c, carry
  pop af
  add hl, bc
  pop bc
  ld (de), a
  inc de
  ret

carry:
  dec bc
  ret



main:
    ld sp, 1000
    ld hl, sys_vb_begin 

    ; counter: from ascii 0 - 1
    ld b, 47

loop:
    ld hl, sys_vb_begin 
    call sys_video_clear    

    ld a, 58
    inc b
    cp b
    jp z, end

    ld a, b
    call sys_print_char

    jp loop

end:
    halt
