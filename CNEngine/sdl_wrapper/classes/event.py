from sdl2 import (
    SDL_Event,
    SDL_PollEvent,

    SDL_MOUSEBUTTONDOWN,
    SDL_MOUSEBUTTONUP,
    SDL_MOUSEMOTION,
    SDL_MOUSEWHEEL,
    SDL_KEYUP,
    SDL_KEYDOWN,

    SDL_WINDOWEVENT
)
from ctypes import byref

from ..locals.window_header import EXISTING_WINDOWS
from ..locals.event_header import EVENT_SDL

class Event(object):
    def __init__(self, event_type: int, x: int, y: int, key: int) -> None:
        self.type = event_type
        self.x = x
        self.y = y
        self.key  = key

def _get_event(event_type):
    if (event_type in EVENT_SDL):
        return (EVENT_SDL[event_type])

def _get_event_arguments(event) -> tuple:
    if (event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP):
        return (event.button.x, event.button.y, event.button.button)
    if (event.type == SDL_MOUSEMOTION):
        return (event.motion.x, event.motion.y, 0)
    if (event.type == SDL_MOUSEWHEEL):
        return (event.wheel.x, event.wheel.y, 0)
    if (event.type == SDL_KEYUP):
        return (0, 0, event.key.keysym.sym)
    if (event.type == SDL_KEYDOWN):
        return (0, 0, event.key.keysym.sym)
    return (0, 0, 0)

def fetch_events():
    event = SDL_Event()

    for win in EXISTING_WINDOWS.values():
        for item in EVENT_SDL:
            win.events[EVENT_SDL[item]] = None

    while SDL_PollEvent(byref(event)) != 0:
        window_id = event.window.windowID

        if (window_id in EXISTING_WINDOWS):
            EXISTING_WINDOWS[window_id].events[_get_event(event.type if event.type != SDL_WINDOWEVENT else event.window.event)] = Event(event.type, *_get_event_arguments(event))

        else:
            for win in EXISTING_WINDOWS.values():
                win.events[event.type] = Event(event.type, *_get_event_arguments(event))
