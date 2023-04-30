  .cr Z80

; beginning of bios
bios_def_bios_begin = 0xFA00

; beginning of the video buffer
bios_def_vb_begin = 0xFE00

; puts a character into memory pointed by HL
; params:
;   - A, ascii character
bios_def_vb_print_char = bios_def_bios_begin + 10
