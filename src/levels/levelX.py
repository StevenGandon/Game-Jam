from CNEngine import *
from .objects.end_animation import EndAnimation

class ChanginScreenCOlor(Loader):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.interface = interface
        self.animation_frame = 0
        self.indicator_index = 0
        self.size = 20
        self.backgroundColor = 0

    def event(self, window) -> None:
        super().event(window)

        key_press = window.get_event(EVENT_KEY_UP)
        if key_press:
            if SDLK_F10 in key_press.key:
                self.backgroundColor += 10
                if (self.backgroundColor > 255):
                    self.backgroundColor = 255
            if SDLK_F11 in key_press.key:
                self.backgroundColor -= 10
                if (self.backgroundColor < 0):
                    self.backgroundColor = 0

    def draw(self, screen):
        screen.clear((self.backgroundColor, self.backgroundColor, self.backgroundColor))

    def destroy(self) -> None:
        super().destroy()

class Lever(Object):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.animation: int = 0
        self.animation_reverse = False
        self.interface = interface
        self.background = get_texture(f"{ROOT}/assets/ressources/UI/9k.png")
        self.window = interface.window
        self.backgroundColor = 0
        self.vector = Vector2(interface.window.video_mode.size.x / 2 - 25, interface.window.video_mode.size.y / 2 - 25)


    def event(self, window) -> None:
        super().event(window)

        key_press = window.get_event(EVENT_KEY_UP)
        if key_press:
            if SDLK_F10 in key_press.key:
                self.backgroundColor += 10
                if (self.backgroundColor > 255):
                    self.backgroundColor = 255
            if SDLK_F11 in key_press.key:
                self.backgroundColor -= 10
                if (self.backgroundColor < 0):
                    self.backgroundColor = 0
        self.background.set_alpha(self.backgroundColor)

    def draw(self, screen):
        screen.blit_scaled(self.background, self.vector, self.vector, ratios = Vector2(0.35, 0.35))

def build_levelX(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")
    interface.add_element(ChanginScreenCOlor(interface))
    interface.add_element(Lever(interface))

    interface.add_gui(Button(interface.window.video_mode.size.x / 2 - 25, interface.window.video_mode.size.y / 2 - 25, 50, 50, lambda *args: interface.add_gui(EndAnimation(interface))))

    interface.window.set_closable(False)
    return interface
