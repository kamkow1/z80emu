; params:
;   - hl = number
;   - de = ptr to out buffer (5 bytes)

num16_to_ascii:
  ld	bc,-10000
	call	Num1
	ld	bc,-1000
	call	Num1
	ld	bc,-100
	call	Num1
	ld	c,-10
	call	Num1
	ld	c,b
Num1:
	ld	a,'0'-1
Num2:
	inc	a
	add	hl,bc
	jr	c,Num2
	sbc	hl,bc

	ld	(de),a
	inc	de
	ret
