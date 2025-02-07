def get_flag(flags: int, get: int) -> int:
    return ((flags & get) > 0)

def set_flag(flags: int, new: int) -> int:
    return (flags | new)
