from ..sdl_wrapper import Texture, Vector2, Window

from .object import Object

class Image(Object):
    def __init__(self, x: int, y: int, image: Texture) -> None:
        super().__init__(x, y)

        self.image = image

    def draw(self, screen: Window) -> None:
        screen.blit(self.image, Vector2(self.x, self.y))
