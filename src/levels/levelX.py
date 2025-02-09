from CNEngine import *
from .objects.end_animation import EndAnimation

class ChanginScreenCOlor(Loader):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.activated = False
        self.interface = interface
        self.animation_frame = 0
        self.indicator_index = 0
        self.size = 20
        self.backgroundColor = 0
        self.lever = get_texture(f"{ROOT}/assets/ressources/UI/9k.png")
        self.vector = Vector2(interface.window.video_mode.size.x / 2 - 25, interface.window.video_mode.size.y / 2 - 25)

    def changeLever(self) -> None:
        if (not self.activated):
            self.change_lever_image(f"{ROOT}/assets/ressources/UI/9k2.png")
            self.interface.add_gui(EndAnimation(self.interface))
            self.activated = True

    def event(self, window) -> None:
        super().event(window)

        key_press = window.get_event(EVENT_KEY_UP)
        mouse_press = window.get_event(EVENT_MOUSE_DOWN)
        if key_press:
            if SDLK_F10 in key_press.key:
                self.backgroundColor += 10
                if (self.backgroundColor > 255):
                    self.backgroundColor = 255
            if SDLK_F11 in key_press.key:
                self.backgroundColor -= 10
                if (self.backgroundColor < 0):
                    self.backgroundColor = 0
        if mouse_press:
            print(mouse_press.key)
            if (1 in mouse_press.key and self.backgroundColor != 255):
                self.interface.show_error_window("on y voie rien")

        self.lever.set_alpha(self.backgroundColor)
        if (self.backgroundColor == 255):
            self.interface.add_gui(Button(self.interface.window.video_mode.size.x / 2 - 25, self.interface.window.video_mode.size.y / 2 - 25, 50, 50, lambda _: self.changeLever()))


    def draw(self, screen):
        screen.clear((self.backgroundColor, self.backgroundColor, self.backgroundColor))
        screen.blit_scaled(self.lever, self.vector, self.vector, ratios = Vector2(0.35, 0.35))

    def change_lever_image(self, new_image_path):
        self.lever = get_texture(new_image_path)

    def destroy(self) -> None:
        super().destroy()



def build_levelX(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")

    interface.add_element(ChanginScreenCOlor(interface))
    interface.window.set_closable(False)
    return interface
