  .cr Z80

bjt_item_len = 3

; beginning of bios
sys_bios_begin = 0xFA00

; beginning of the video buffer
sys_vb_begin = 0xFE00

; params:
; hl = char to print
sys_print_char = sys_bios_begin

; params:
; bc = ptr to beginning of string
; notes:
; calls to `sys_print_char` under the hood
sys_print_str = sys_print_char+bjt_item_len
