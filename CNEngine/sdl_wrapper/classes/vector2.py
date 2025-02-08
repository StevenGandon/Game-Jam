class Vector2(object):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, __index):
        return (self.x, self.y)[__index]
    
    def __setitem__(self, __index, __value):
        values: list = [self.x, self.y]

        values[__index] = __value
        self.x, self.y = values
    
    def __repr__(self) -> str:
        return (f"(x={self.x}, y={self.y})")

    def __mul__(self, other: object) -> object:
        return Vector2(self.x * other.x, self.y * other.y)

    def to_negative(self) -> object:
        return Vector2(-self.x, -self.y)
    
    def to_int(self) -> object:
        return (Vector2(int(self.x), int(self.y)))
