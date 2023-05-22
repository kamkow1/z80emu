  .cr Z80
  .tf out.bin, BIN
  .lf out.lst
  .sf out.sym
  .in bios/bios_defs.inc

main:
  ld sp, 1000
  ; init video
  ld hl, sys_vb_begin

  ; 1. read from port 0xA
  ; the data comes from the python plugin
  ; 2. display the data on the screen
  in a, (0xA) ; K
  call sys_print_char
  in a, (0xB) ; A
  call sys_print_char
  in a, (0xC) ; M
  call sys_print_char
  in a, (0xD) ; I
  call sys_print_char
  in a, (0xE) ; L
  call sys_print_char
  in a, (0xF) ; !
  call sys_print_char

  call sys_video_clear

  jp main
