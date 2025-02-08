from .vector2 import Vector2

class VideoMode(object):
    def __init__(self, size: Vector2, position: Vector2, depht: int, flags: int = 0x00, vsync: bool = False, acceleration: bool = True) -> None:
        self.size: Vector2 = size
        self.position: Vector2 = position

        self.depht: int = depht

        self.flags: int = flags

        self.vsync: bool = vsync
        self.acceleration: bool = acceleration
