from .object import Object
from .texture import Texture
from ..sdl_wrapper import Vector2

class Rectangle(Object):
    def __init__(self, x: int, y: int, size_x: int, size_y: int, color: tuple) -> None:
        super().__init__(x, y)

        self.size_x = size_x
        self.size_y = size_y

        self.old_rect = [self.size_x, self.size_y]

        self.image = Texture(Vector2(size_x, size_y))
        self.color = color

        self.image.clear(color)

    def update(self, delta_time: int):
        if (self.size_x != self.old_rect[0] or self.size_y != self.old_rect[1]):
            self.old_rect[0] = self.size_x
            self.old_rect[1] = self.size_y

            self.image.destroy()
            self.image = Texture(Vector2(self.size_x, self.size_y).to_int())

            self.image.clear(self.color)

    def draw(self, screen) -> None:
        screen.blit(self.image, Vector2(self.x, self.y))
