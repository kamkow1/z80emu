import os
import sdl2, sdl2.ext


sdl2.ext.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = sdl2.ext.Window("z80emu", size=(WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.show()
RENDERER =  sdl2.ext.Renderer(WINDOW, flags=sdl2.SDL_RENDERER_SOFTWARE)

WHITE_RGBA = (0xFF, 0xFF, 0xFF, 0xFF)
BLACK_RGBA = (0x00, 0x00, 0x00, 0xFF)
FONT_FILE = "ProggyClean.ttf"
_font_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../assets",
    FONT_FILE)
FONT = sdl2.ext.FontTTF(_font_path, "16px", WHITE_RGBA)


def video_update(self):
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            return False

    # render video buffer
    # vb: 0xFE01 -> 0xFFFF
    # 0xFFFF - 0xFE01 = 30 x 17
    ascii_text = ""
    for row in range(17):
        for col in range(30):
            # addresses are measured from the end of RAM (0xFFFF)
            cell_addr = 0xFFFF - (17 * row + col) - 1
            ram_cell = self.ram[cell_addr]
            ascii_text += chr(ram_cell)

    if all(c == ascii_text[0] for c in ascii_text):
        ascii_text = "No text to display..."

    rendered_text = FONT.render_text(ascii_text, width=WINDOW_WIDTH)
    texture = sdl2.ext.Texture(RENDERER, rendered_text)
    RENDERER.clear(BLACK_RGBA)
    RENDERER.copy(texture, dstrect=(10, 10))
    RENDERER.present()

    WINDOW.refresh()

    return True


def video_end(self):
    FONT.close()
    RENDERER.destroy()
    WINDOW.close()
    sdl2.ext.quit()
