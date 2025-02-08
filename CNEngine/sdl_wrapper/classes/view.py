from .vector2 import Vector2

class View(object):
    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)

        self.rotation: int = 0
        self.zoom: float = 1

    def set_zoom(self, zoom: float) -> None:
        self.zoom = zoom

    def set_position(self, position: Vector2) -> None:
        self.position = position

    def set_rotation(self, rotation: float) -> None:
        self.rotation = rotation % 361
