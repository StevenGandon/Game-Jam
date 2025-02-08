from sdl2 import SDL_SetCursor, SDL_SYSTEM_CURSOR_HAND, SDL_SYSTEM_CURSOR_ARROW, SDL_CreateSystemCursor

from ..sdl_wrapper import Window, EVENT_MOUSE_MOVE, EVENT_MOUSE_DOWN, EVENT_MOUSE_UP

from .object import Object

class Button(Object):
    def __init__(self, x, y, size_x, size_y, callback) -> None:
        super().__init__(x, y)

        self.size_x = size_x
        self.size_y = size_y
        self.callback = callback

        self.hover = False
        self.cursor = False

        self.click = False
        self.release = False

        self.click_pos = (0, 0)

    def event(self, window: Window):
        event = window.get_event(EVENT_MOUSE_MOVE)
        if (event and event.x >= self.x and event.x <= self.x + self.size_x and event.y >= self.y and event.y <= self.y + self.size_y):
            self.hover = True
        elif (event):
            self.hover = False

        if (self.hover and window.get_event(EVENT_MOUSE_DOWN)):
            self.click = True
        if (self.click and window.get_event(EVENT_MOUSE_UP)):
            self.click = False
            if (self.hover):
                self.release = True
                self.click_pos = (window.get_event(EVENT_MOUSE_UP).x, window.get_event(EVENT_MOUSE_UP).y)

    def update(self, delta_time):
        if (self.hover and not self.cursor):
            SDL_SetCursor(SDL_CreateSystemCursor(SDL_SYSTEM_CURSOR_HAND))
            self.cursor = True
        if (self.cursor and not self.hover):
            SDL_SetCursor(SDL_CreateSystemCursor(SDL_SYSTEM_CURSOR_ARROW))
            self.cursor = False

        if (self.release):
            self.release = False
            self.callback(self.click_pos)