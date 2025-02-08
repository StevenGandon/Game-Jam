from sdl2 import (
    SDL_BlitSurface,
    SDL_FreeSurface,
    SDL_FillRect,
    SDL_CreateRGBSurface,
    SDL_ConvertSurface,
    SDL_MapRGB,
    SDL_MapRGBA,

    SDL_SWSURFACE,
    SDL_Surface,
    SDL_Rect,
    SDL_BlitScaled,
    SDL_SetSurfaceAlphaMod
)

from sdl2.sdlimage import (
    IMG_Load
)

from .vector2 import Vector2
from .mask import (RGBAMask, RGBMask)

class Texture(object):
    def __init__(self, size: Vector2 = None, depht: int = 32, alpha: bool = True) -> None:
        self.size = size
        self.depht = depht
        self.rgb_mask = (RGBAMask() if alpha else RGBMask())

        if (size is None):
            self.surface = None
            return

        self.surface = SDL_CreateRGBSurface(SDL_SWSURFACE, *size, depht, *self.rgb_mask)

    def __repr__(self) -> str:
        return (f"size_x = {self.size.x}, size_y = {self.size.y}, depht = {self.depht}, mask = {self.rgb_mask}")

    def __del__(self):
        self.destroy()

    def draw_rect(self, position: Vector2, size: Vector2, color: tuple) -> None:
        if (self.surface is None):
            return

        SDL_FillRect(self.surface, SDL_Rect(*position, *size), SDL_MapRGBA(self.surface.contents.format, *color) if len(color) == 4 else SDL_MapRGB(self.surface.contents.format, *color))

    def clear(self, color: tuple) -> None:
        if (self.surface is None):
            return

        SDL_FillRect(self.surface, None, SDL_MapRGBA(self.surface.contents.format, *color) if len(color) == 4 else SDL_MapRGB(self.surface.contents.format, *color))

    def set_alpha(self, alpha: int):
        if (self.surface is None):
            return

        SDL_SetSurfaceAlphaMod(self.surface, alpha)

    def blit(self, other, position: Vector2 = None, size: Vector2 = None, from_pos: Vector2 = None, ratios: Vector2 = None) -> None:
        if (self.surface is None):
            return

        if (not ratios):
            ratios = Vector2(1, 1)
        if (not position):
            position = Vector2(0, 0)
        if (not size):
            size = (other.size)
        if (not from_pos):
            from_pos = Vector2(0, 0)

        SDL_BlitSurface(other.surface, SDL_Rect(*(from_pos.to_int()), *((size * ratios).to_int())), self.surface, SDL_Rect(*(position.to_int()), *(self.size.to_int())))

    def blit_scaled(self, other, position: Vector2 = None, size: Vector2 = None, from_pos: Vector2 = None, ratios: Vector2 = None) -> None:
        if (self.surface is None):
            return

        if (not ratios):
            ratios = Vector2(1, 1)
        if (not position):
            position = Vector2(0, 0)
        if (not size):
            size = (other.size)
        if (not from_pos):
            from_pos = Vector2(0, 0)

        SDL_BlitScaled(other.surface, SDL_Rect(*(from_pos.to_int()), *((size).to_int())), self.surface, SDL_Rect(*((position).to_int()), *((size * ratios).to_int())))

    def optimize_blit(self, other):
        SDL_ConvertSurface(self.surface, other.surface.contents.format, 0)

    @staticmethod
    def from_sdl_surface(surface) -> object:
        self = Texture()

        if (not surface):
            return (self)

        self.surface = surface
        self.size = Vector2(surface.contents.w, surface.contents.h)
        self.depht = surface.contents.format.contents.BitsPerPixel

        self.rgb_mask.r_mask = self.surface.contents.format.contents.Rmask
        self.rgb_mask.g_mask = self.surface.contents.format.contents.Gmask
        self.rgb_mask.b_mask = self.surface.contents.format.contents.Bmask
        self.rgb_mask.a_mask = self.surface.contents.format.contents.Amask
        self.rgb_mask.bits = self.surface.contents.format.contents.BytesPerPixel

        return (self)

    @staticmethod
    def from_file(path: str) -> object:
        surface = IMG_Load(path.encode())

        if (not surface):
            surface = SDL_CreateRGBSurface(SDL_SWSURFACE, 100, 100, 32, *RGBMask())
            SDL_FillRect(surface, SDL_Rect(0, 0, 100, 100), SDL_MapRGB(surface.contents.format, 0, 0, 0))
            SDL_FillRect(surface, SDL_Rect(50, 0, 50, 50), SDL_MapRGB(surface.contents.format, 106, 22, 171))
            SDL_FillRect(surface, SDL_Rect(0, 50, 50, 50), SDL_MapRGB(surface.contents.format, 106, 22, 171))

        self = Texture()

        self.surface = surface
        self.size = Vector2(surface.contents.w, surface.contents.h)
        self.depht = surface.contents.format.contents.BitsPerPixel

        self.rgb_mask.r_mask = self.surface.contents.format.contents.Rmask
        self.rgb_mask.g_mask = self.surface.contents.format.contents.Gmask
        self.rgb_mask.b_mask = self.surface.contents.format.contents.Bmask
        self.rgb_mask.a_mask = self.surface.contents.format.contents.Amask
        self.rgb_mask.bits = self.surface.contents.format.contents.BytesPerPixel

        return (self)

    def destroy(self) -> None:
        if (self.surface is None):
            return

        SDL_FreeSurface(self.surface)
        self.surface = None

