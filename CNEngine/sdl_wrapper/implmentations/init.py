from sdl2 import (
    SDL_Init,
    SDL_Quit,
    SDL_GetError,

    SDL_INIT_VIDEO,
    SDL_INIT_AUDIO,
    SDL_INIT_GAMECONTROLLER,
    SDL_INIT_EVENTS,
    SDL_INIT_TIMER,
    SDL_INIT_HAPTIC,
    SDL_INIT_NOPARACHUTE,
    SDL_INIT_JOYSTICK,
    SDL_INIT_SENSOR
)
from sdl2.sdlimage import (
    IMG_Init,
    IMG_Quit,
    IMG_GetError,

    IMG_INIT_JPG,
    IMG_INIT_PNG,
    IMG_INIT_WEBP,
    IMG_INIT_AVIF,
    IMG_INIT_JXL,
    IMG_INIT_TIF
)

from ..common.flags import get_flag

from ..locals.init_header import (
    INITED_VALUES,

    INIT_VIDEO,
    INIT_AUDIO,
    INIT_GAME_CONTROLLER,
    INIT_EVENT,
    INIT_TIMER,
    INIT_HAPSTIC,
    INIT_NOPARACHUTE,
    INIT_JOYSTICK,
    INIT_SENSOR,

    INIT_IMG_JPG,
    INIT_IMG_PNG,
    INIT_IMG_WEBP,
    INIT_IMG_AVIF,
    INIT_IMG_JXL,
    INIT_IMG_TIF
)
from ..locals.common_header import ERROR_STACK

def init(flags: int) -> None:
    if (not INITED_VALUES[0] and get_flag(flags, INIT_VIDEO)):
        if (SDL_Init(SDL_INIT_VIDEO) == 0):
            INITED_VALUES[0] = True
        else:
            ERROR_STACK.append(f'Failed to initialize video, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[1] and get_flag(flags, INIT_AUDIO)):
        if (SDL_Init(SDL_INIT_AUDIO) == 0):
            INITED_VALUES[1] = True
        else:
            ERROR_STACK.append(f'Failed to initialize audio, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[2] and get_flag(flags, INIT_GAME_CONTROLLER)):
        if (SDL_Init(SDL_INIT_GAMECONTROLLER) == 0):
            INITED_VALUES[2] = True
        else:
            ERROR_STACK.append(f'Failed to initialize gamecontroller, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[3] and get_flag(flags, INIT_EVENT)):
        if (SDL_Init(SDL_INIT_EVENTS) == 0):
            INITED_VALUES[3] = True
        else:
            ERROR_STACK.append(f'Failed to initialize events, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[4] and get_flag(flags, INIT_TIMER)):
        if (SDL_Init(SDL_INIT_TIMER) == 0):
            INITED_VALUES[4] = True
        else:
            ERROR_STACK.append(f'Failed to initialize timer, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[5] and get_flag(flags, INIT_HAPSTIC)):
        if (SDL_Init(SDL_INIT_HAPTIC) == 0):
            INITED_VALUES[5] = True
        else:
            ERROR_STACK.append(f'Failed to initialize haptic, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[6] and get_flag(flags, INIT_NOPARACHUTE)):
        if (SDL_Init(SDL_INIT_NOPARACHUTE) == 0):
            INITED_VALUES[6] = True
        else:
            ERROR_STACK.append(f'Failed to initialize no parachute, SDL2 error:\n{SDL_GetError()}')
    
    if (not INITED_VALUES[7] and get_flag(flags, INIT_JOYSTICK)):
        if (SDL_Init(SDL_INIT_JOYSTICK) == 0):
            INITED_VALUES[7] = True
        else:
            ERROR_STACK.append(f'Failed to initialize joystick, SDL2 error:\n{SDL_GetError()}')

    if (not INITED_VALUES[8] and get_flag(flags, INIT_SENSOR)):
        if (SDL_Init(SDL_INIT_SENSOR) == 0):
            INITED_VALUES[8] = True
        else:
            ERROR_STACK.append(f'Failed to initialize sensors, SDL2 error:\n{SDL_GetError()}')


    if (not INITED_VALUES[9] and get_flag(flags, INIT_IMG_JPG)):
        if (IMG_Init(IMG_INIT_JPG) & IMG_INIT_JPG == IMG_INIT_JPG):
            INITED_VALUES[9] = True
        else:
            ERROR_STACK.append(f'Failed to initialize JPG, SDL2 error:\n{IMG_GetError()}')

    if (not INITED_VALUES[10] and get_flag(flags, INIT_IMG_PNG)):
        if (IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG == IMG_INIT_PNG):
            INITED_VALUES[10] = True
        else:
            ERROR_STACK.append(f'Failed to initialize PNG, SDL2 error:\n{IMG_GetError()}')

    if (not INITED_VALUES[11] and get_flag(flags, INIT_IMG_WEBP)):
        if (IMG_Init(IMG_INIT_WEBP) & IMG_INIT_WEBP == IMG_INIT_WEBP):
            INITED_VALUES[11] = True
        else:
            ERROR_STACK.append(f'Failed to initialize WEBP, SDL2 error:\n{IMG_GetError()}')

    if (not INITED_VALUES[12] and get_flag(flags, INIT_IMG_AVIF)):
        if (IMG_Init(IMG_INIT_AVIF) & IMG_INIT_AVIF == IMG_INIT_AVIF):
            INITED_VALUES[12] = True
        else:
            ERROR_STACK.append(f'Failed to initialize AVIF, SDL2 error:\n{IMG_GetError()}')

    if (not INITED_VALUES[13] and get_flag(flags, INIT_IMG_JXL)):
        if (IMG_Init(IMG_INIT_JXL) & IMG_INIT_JXL == IMG_INIT_JXL):
            INITED_VALUES[13] = True
        else:
            ERROR_STACK.append(f'Failed to initialize JXL, SDL2 error:\n{IMG_GetError()}')

    if (not INITED_VALUES[14] and get_flag(flags, INIT_IMG_TIF)):
        if (IMG_Init(IMG_INIT_TIF) & IMG_INIT_TIF == IMG_INIT_TIF):
            INITED_VALUES[14] = True
        else:
            ERROR_STACK.append(f'Failed to initialize TIF, SDL2 error:\n{IMG_GetError()}')

def has_error() -> bool:
    return (len(ERROR_STACK) != 0)

def get_error() -> str:
    if (has_error()):
        return ERROR_STACK.pop()
    else:
        return None

def quit():
    IMG_Quit()
    SDL_Quit()
