from sdl2.ext.ttf import FontTTF
from sdl2 import SDL_ConvertSurfaceFormat, SDL_PIXELFORMAT_RGBA32, SDL_FreeSurface

from ..sdl_wrapper import Texture, Vector2, Window
from ..locals import CACHED_FONTS, RESSOURCES

from .object import Object

class Text(Object):
    def __init__(self, x, y, text, size=14, color=(255, 255, 255), font=f"{RESSOURCES}/font/Inter.ttf") -> None:
        super().__init__(x, y)

        font = font.replace('\\', '/')
        entry = f"{font.split('/')[-1]}{size}{color}"

        if (entry) in CACHED_FONTS:
            self.font = CACHED_FONTS[entry]
        else:
            self.font = FontTTF(font, size, color)
            CACHED_FONTS[entry] = self.font

        self.base_font_size = size
        self.base_font_name = font
        self.text = text

        temp = self.font.render_text(self.text)
        self.texture: Texture = Texture.from_sdl_surface(SDL_ConvertSurfaceFormat(temp, SDL_PIXELFORMAT_RGBA32, 0))
        SDL_FreeSurface(temp)

    def set_text(self, text):
        self.text = text

        self.texture.destroy()
        temp = self.font.render_text(self.text)
        self.texture: Texture = Texture.from_sdl_surface(SDL_ConvertSurfaceFormat(temp, SDL_PIXELFORMAT_RGBA32, 0))
        SDL_FreeSurface(temp)

    def set_color(self, color):
        font = self.base_font_name.replace('\\', '/')
        entry = f"{font.split('/')[-1]}{self.base_font_size}{color}"

        if (entry) in CACHED_FONTS:
            self.font = CACHED_FONTS[entry]
        else:
            self.font = FontTTF(font, self.base_font_size, color)
            CACHED_FONTS[entry] = self.font

        self.texture.destroy()
        temp = self.font.render_text(self.text)
        self.texture: Texture = Texture.from_sdl_surface(SDL_ConvertSurfaceFormat(temp, SDL_PIXELFORMAT_RGBA32, 0))
        SDL_FreeSurface(temp)

    def draw(self, screen: Window):
        screen.blit(self.texture, Vector2(self.x, self.y))

    def destroy(self) -> None:
        super().destroy()

        self.texture.destroy()

    def __del__(self):
        self.destroy()
