from ...interface import *
from ...sdl_wrapper import (
    VideoMode,
    Vector2,

    WINDOW_POS_CENTER
)
from sdl2 import SDL_WINDOWPOS_UNDEFINED
from ...locals import RESSOURCES

class ErrorInterface(Interface):
    def __init__(self, title: str = "Error", error_message: str = "") -> None:
        super().__init__(title, VideoMode(Vector2(int(45 + len(error_message) * 14 * 0.6 + 30), 100), Vector2(SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED), 32), get_texture(f"{RESSOURCES}/UI/error-icon.png"))

        self.error_message = error_message
        self.error_icon = get_texture(f"{RESSOURCES}/UI/error-icon.png")
        self.text = Text(15 + self.error_icon.size.x + 15, self.window.video_mode.size.y / 2 - 7, error_message, 14, (15, 15, 15))

    def draw(self):
        self.window.clear((235, 235, 235))
        self.window.blit(self.error_icon, Vector2(15, self.window.video_mode.size.y / 2 - self.error_icon.size.y / 2))
        self.text.draw(self.window)

    def destroy(self) -> None:
        self.text.destroy()

        super().destroy()
