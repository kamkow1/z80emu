  .cr Z80

bjt_item_len = 3

; beginning of bios
sys_bios_begin = 0xFA00

sys_print_char = sys_bios_begin
sys_print_str = sys_print_char+bjt_item_len

; beginning of the video buffer
sys_vb_begin = 0xFE00

