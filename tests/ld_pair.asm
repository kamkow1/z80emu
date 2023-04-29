  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym

main:
  ld hl, 69
  ld (hl), 56

  ; a
  ld hl, 200
  ld a, 10
  ld (hl), a

  ; b
  ld hl, 225
  ld b, 11
  ld (hl), b

  ; c
  ld hl, 250
  ld c, 12
  ld (hl), c

  ; d
  ld hl, 275
  ld d, 13
  ld (hl), d

  ; e
  ld hl, 300
  ld e, 14
  ld (hl), e

  ; h
  ld hl, 325
  ld h, 15
  ld (hl), h

  ; l
  ld hl, 350
  ld l, 16
  ld (hl), l


  ld a, (hl)
  ld (bc), a


  ld hl, 105 
  ld (400), hl

  ld a, 1056
  ld (420), a

  halt

