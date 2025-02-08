from sdl2 import (
    SDL_GetTicks,
    SDL_Delay
)

class Clock(object):
    def __init__(self) -> None:
        self.old_time = SDL_GetTicks()

    def tick(self, fps = -1) -> int:
        execution_time = 1000.0 / fps
        delta = SDL_GetTicks() - self.old_time

        if (fps == -1):
            self.old_time = SDL_GetTicks()
            return (delta)
        else:
            sleep_time = execution_time - delta

            if (sleep_time >= 1.0):
                SDL_Delay(round(sleep_time))

            self.old_time = SDL_GetTicks()
            return (delta + sleep_time if sleep_time > 0.0 else delta)
