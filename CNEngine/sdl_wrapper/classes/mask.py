def calculate_mask(size: int, pos: int, value: int) -> int:
    shift: int = (((size - 2) * 4) - (pos * 4))

    if (shift < 0):
        raise (ValueError("Invalid mask position, not enough bits"))
    return (value << shift)

class RGBAMask(object):
    def __init__(self, r_pos: int = 0x00, g_pos: int = 0x02, b_pos: int = 0x04, a_pos: int = 0x06, bits: int = 8, values: tuple = (0xFF, 0xFF, 0xFF, 0xFF)) -> None:
        self.r_mask = calculate_mask(bits, r_pos, values[0])
        self.g_mask = calculate_mask(bits, g_pos, values[1])
        self.b_mask = calculate_mask(bits, b_pos, values[2])
        self.a_mask = calculate_mask(bits, a_pos, values[3])

        self.bits = bits

    def __repr__(self) -> str:
        return (f"[r = {self.r_mask}, g = {self.g_mask}, b = {self.b_mask}, a = {self.a_mask}] ({self.bits} bits)")

    def __iter__(self) -> iter:
        return iter((self.r_mask, self.g_mask, self.b_mask, self.a_mask))

class RGBMask(RGBAMask):
    def __init__(self, r_pos: int = 0x00, g_pos: int = 0x02, b_pos: int = 0x04, bits: int = 6, values: tuple = (0xFF, 0xFF, 0xFF)) -> None:
        super().__init__(r_pos, g_pos, b_pos, 0x00, bits, (values[0], values[1], values[2], 0x00))
