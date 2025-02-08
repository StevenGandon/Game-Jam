from sdl2 import (
    SDL_CreateWindow,
    SDL_GetWindowSurface,
    SDL_DestroyWindow,
    SDL_UpdateWindowSurface,
    SDL_GetWindowID,
    SDL_RenderSetVSync,
    SDL_CreateRenderer,
    SDL_DestroyRenderer,
    # SDL_CreateShapedWindow,
    SDL_SetWindowResizable,
    SDL_HideWindow,
    SDL_ShowWindow,
    SDL_SetWindowIcon,
    # SDL_SetWindowShape,

    SDL_RENDERER_ACCELERATED,
    SDL_RENDERER_PRESENTVSYNC,

    SDL_WINDOW_SHOWN,

    SDL_LockSurface,
    SDL_UnlockSurface,
    SDL_MapRGB,
    SDL_SetWindowTitle
)

from ..locals.window_header import EXISTING_WINDOWS, WINDOW_POS_CENTER
from ..locals.event_header import EVENT_QUIT, EVENT_CLOSE, EVENT_ITERABLE

from .texture import Texture
from .view import View
from .video_mode import VideoMode
from .vector2 import Vector2
from .event import Event
import math
import ctypes

class Window(object):
    def __init__(self, title: str = "New Window", video_mode: VideoMode = VideoMode(Vector2(925, 600), Vector2(WINDOW_POS_CENTER, WINDOW_POS_CENTER), 32, 0, False, True), icon: Texture = None) -> None:
        self.window = SDL_CreateWindow(
            title.encode(errors="ignore"),
            *video_mode.position,
            *video_mode.size,
            SDL_WINDOW_SHOWN
        )

        SDL_SetWindowResizable(self.window, False)

        self.renderer = SDL_CreateRenderer(self.window, -1, (SDL_RENDERER_PRESENTVSYNC if video_mode.vsync else 0) | (SDL_RENDERER_ACCELERATED if video_mode.acceleration else 0))
        self.id = SDL_GetWindowID(self.window)

        EXISTING_WINDOWS[self.id] = self

        self.icon = icon
        self.video_mode = video_mode
        self.texture = Texture.from_sdl_surface(SDL_GetWindowSurface(self.window))
        self.view = View()
        self.events = {item: None for item in EVENT_ITERABLE}

        self.is_closable = True
        self.hidden = False

        if (self.icon):
            SDL_SetWindowIcon(self.window, self.icon.surface)

    def __del__(self):
        self.destroy()

    def set_vsync(self, value: bool) -> None:
        self.video_mode.vsync = value

        SDL_RenderSetVSync(self.renderer, int(self.video_mode.vsync))

    def get_vsync(self) -> bool:
        return (self.video_mode.vsync)

    def set_closable(self, value: bool) -> None:
        self.is_closable = value

    def get_closable(self) -> bool:
        return (self.is_closable)

    def check_event(self, event: int) -> None:
        events = self.events

        return (event in events and events[event] is not None)

    def get_event(self, event: int) -> Event:
        if (self.check_event(event)):
            return (self.events[event])
        return None

    def update(self) -> None:
        if (self.is_closable):
            if (self.get_event(EVENT_QUIT) or self.get_event(EVENT_CLOSE)):
                self.destroy()

    def blit(self, other, position: Vector2 = None, size: Vector2 = None, from_pos: Vector2 = None, ratios: Vector2 = None) -> None:
        self.texture.blit(other, position, size, from_pos, ratios)

    def blit_scaled(self, other, position: Vector2 = None, size: Vector2 = None, from_pos: Vector2 = None, ratios: Vector2 = None) -> None:
        self.texture.blit_scaled(other, position, size, from_pos, ratios)

    def clear(self, color: tuple = (0, 0, 0)) -> None:
        self.texture.clear(color)

    def draw(self) -> None:
        SDL_UpdateWindowSurface(self.window)

    def set_hidden(self, state: bool) -> None:
        self.hidden: bool = state

        if (state):
            SDL_HideWindow(self.window)
        else:
            SDL_ShowWindow(self.window)

    def get_hidden(self) -> bool:
        return (self.hidden)

    def set_title(self, title: str):
        SDL_SetWindowTitle(self.window, title)

    def draw_circle(self, center: tuple, radius: int, color: tuple, thickness: int = 0) -> None:
        surface = self.texture.surface
        if not surface or SDL_LockSurface(surface) != 0:
            return

        if thickness <= 0:
            self._draw_filled_circle_surface(center, radius, color, surface)
        else:
            for t in range(thickness):
                current_radius = radius - t
                if current_radius > 0:
                    self._draw_circle_outline_surface(center, current_radius, color, surface)
        SDL_UnlockSurface(surface)

    def _draw_circle_outline_surface(self, center: tuple, radius: int, color: tuple, surface) -> None:
        x0, y0 = center
        x = radius
        y = 0
        err = 0

        while x >= y:
            self._put_pixel_surface(surface, x0 + x, y0 + y, color)
            self._put_pixel_surface(surface, x0 + y, y0 + x, color)
            self._put_pixel_surface(surface, x0 - y, y0 + x, color)
            self._put_pixel_surface(surface, x0 - x, y0 + y, color)
            self._put_pixel_surface(surface, x0 - x, y0 - y, color)
            self._put_pixel_surface(surface, x0 - y, y0 - x, color)
            self._put_pixel_surface(surface, x0 + y, y0 - x, color)
            self._put_pixel_surface(surface, x0 + x, y0 - y, color)
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

    def _draw_filled_circle_surface(self, center: tuple, radius: int, color: tuple, surface) -> None:
        x0, y0 = center
        for y in range(-radius, radius + 1):
            dx = int(math.sqrt(radius * radius - y * y))
            for x in range(-dx, dx + 1):
                self._put_pixel_surface(surface, x0 + x, y0 + y, color)

    def _put_pixel_surface(self, surface, x: int, y: int, color: tuple) -> None:
        if x < 0 or y < 0 or x >= surface.contents.w or y >= surface.contents.h:
            return

        pixel_value = SDL_MapRGB(surface.contents.format, color[0], color[1], color[2])
        pitch = surface.contents.pitch // 4
        index = int(y) * pitch + int(x)
        pixel_ptr = ctypes.cast(surface.contents.pixels, ctypes.POINTER(ctypes.c_uint32))
        pixel_ptr[index] = pixel_value

    def destroy(self) -> None:
        if (self.id in EXISTING_WINDOWS):
            del EXISTING_WINDOWS[self.id]

        self.texture.destroy()

        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)

# class WindowShaped(Window):
#     def __init__(self, title: str = "New Window", video_mode: VideoMode = VideoMode(Vector2(800, 600), Vector2(WINDOW_POS_CENTER, WINDOW_POS_CENTER), 32, 0, False, False)) -> None:
#         self.window = SDL_CreateShapedWindow(
#             title.encode(errors="ignore"),
#             *video_mode.position,
#             *video_mode.size,
#             SDL_WINDOW_SHOWN
#         )

#         self.renderer = SDL_CreateRenderer(self.window, -1, (SDL_RENDERER_PRESENTVSYNC if video_mode.vsync else 0) | (SDL_RENDERER_ACCELERATED if video_mode.acceleration else 0))
#         self.id = SDL_GetWindowID(self.window)

#         EXISTING_WINDOWS[self.id] = self

#         self.video_mode = video_mode
#         self.texture = Texture.from_sdl_surface(SDL_GetWindowSurface(self.window))
#         self.view = View()
#         self.events = {item: None for item in EVENT_ITERABLE}

#         self.is_closable = True
