from sdl2 import SDL_QUIT, SDL_WINDOWEVENT_CLOSE, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEMOTION, SDL_MOUSEWHEEL, SDL_KEYDOWN, SDL_KEYUP

EVENT_QUIT: int = 0x00
EVENT_CLOSE: int = 0x01
EVENT_MOUSE_DOWN: int = 0x02
EVENT_MOUSE_UP: int = 0x03
EVENT_MOUSE_MOVE: int = 0x04
EVENT_MOUSE_SCROLL: int = 0x05
EVENT_KEY_UP: int = 0x06
EVENT_KEY_DOWN: int = 0x07

EVENT_ITERABLE: list = (
    EVENT_QUIT,
    EVENT_CLOSE,
    EVENT_MOUSE_DOWN,
    EVENT_MOUSE_UP,
    EVENT_MOUSE_MOVE,
    EVENT_MOUSE_SCROLL,
    EVENT_KEY_UP,
    EVENT_KEY_DOWN
)

EVENT_SDL: dict = {
    SDL_QUIT: EVENT_QUIT,
    SDL_WINDOWEVENT_CLOSE: EVENT_CLOSE,
    SDL_MOUSEBUTTONDOWN: EVENT_MOUSE_DOWN,
    SDL_MOUSEBUTTONUP: EVENT_MOUSE_UP,
    SDL_MOUSEMOTION: EVENT_MOUSE_MOVE,
    SDL_MOUSEWHEEL: EVENT_MOUSE_SCROLL,
    SDL_KEYUP: EVENT_KEY_UP,
    SDL_KEYDOWN: EVENT_KEY_DOWN
}
