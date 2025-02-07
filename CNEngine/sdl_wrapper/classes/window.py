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

    SDL_WINDOW_SHOWN
)

from ..locals.window_header import EXISTING_WINDOWS, WINDOW_POS_CENTER
from ..locals.event_header import EVENT_QUIT, EVENT_CLOSE, EVENT_ITERABLE

from .texture import Texture
from .view import View
from .video_mode import VideoMode
from .vector2 import Vector2
from .event import Event

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
