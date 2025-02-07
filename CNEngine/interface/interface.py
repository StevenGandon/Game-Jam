from ..sdl_wrapper import Window, VideoMode, Vector2, WINDOW_POS_CENTER
from ..locals import RESSOURCES

from .texture import get_texture
from .object import Object

from itertools import chain

class Interface(object):
    def __init__(self, title: str = "New Interface", video_mode: VideoMode = VideoMode(Vector2(925, 600), Vector2(WINDOW_POS_CENTER, WINDOW_POS_CENTER), 32, 0, False, True), icon = get_texture(f"{RESSOURCES}/UI/icon.png")) -> None:
        self.window = Window(title, video_mode, icon)
        self.window.set_closable(True)

        self.elements = []
        self.gui = []

    def __del__(self) -> None:
        self.destroy()

    def add_element(self, element: Object) -> None:
        if (element not in self.elements):
            self.elements.append(element)

    def add_gui(self, gui: Object) -> None:
        if (gui not in self.gui):
            self.gui.append(gui)

    def events(self) -> None:
        for item in chain(self.elements, self.gui):
            item.event(self.window)

    def update(self, delta_time: float = 0) -> None:
        for item in chain(self.elements, self.gui):
            item.update(delta_time)

    def draw(self) -> None:
        self.window.clear((0, 0, 0))

        for item in chain(self.elements, self.gui):
            item.draw(self.window)

    def destroy(self) -> None:
        self.window.destroy()

        for item in chain(self.elements, self.gui):
            item.destroy()

        self.elements.clear()
