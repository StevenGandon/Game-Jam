from ..locals import CACHED_IMAGE
from ..sdl_wrapper import Texture

def get_texture(path: str):
    if (path in CACHED_IMAGE):
        return (CACHED_IMAGE[path])
    CACHED_IMAGE[path] = Texture.from_file(path)
    return (CACHED_IMAGE[path])
