from .object import Object
from .texture import Texture
from ..sdl_wrapper import Vector2

class Rectangle(Object):
    def __init__(self, x: int, y: int, size_x: int, size_y: int, color: tuple) -> None:
        super().__init__(x, y)

        self.size_x = size_x
        self.size_y = size_y

        self.image = Texture(Vector2(size_x, size_y))

        self.image.clear(color)

    def draw(self, screen) -> None:
        screen.blit(self.image, Vector2(self.x, self.y))
