from CNEngine import *
from .objects.player import Player
from .objects.collision_manager import CollisionManager
from .objects.end_animation import EndAnimation

class MovingBack(Object):
    def __init__(self, x, interface, player):
        super().__init__(x, 0)

        self.interface = interface
        self.background = get_texture(f"{ROOT}/assets/ressources/background-infinite.png")
        self.window = interface.window
        self.player: Player = player

    def event(self, window) -> None:
        super().event(window)

    def update(self, delta_time):
        if (self.player.direction == "right"):
            self.x -= self.player.force_x  * delta_time
        if (self.x + self.background.size.x <= 0):
            self.x = self.window.video_mode.size.x + (self.x + self.background.size.x)

    def draw(self, screen):
        screen.blit(self.background, Vector2(self.x, 0))

class CustomText(Text):
    def __init__(self, x, y, interface):
        super().__init__(x, y, "The end?", 55)

        self.animation = 0
        self.opac = 0

        self.started = False

        self.interface = interface

        self.texture.set_alpha(self.opac)

    def update(self, delta_time):
        self.animation += delta_time

        if (self.animation > 7085):
            self.started = True

        if (self.started and self.animation > 725):
            if (self.opac != 255):
                self.opac += 1
                self.texture.set_alpha(self.opac)

                if (self.opac == 255):
                    self.interface.window.set_closable(True)
        return super().update(delta_time)

    def draw(self, screen):
        return super().draw(screen)

def build_level5(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")

    temp = CollisionManager()

    p = Player(100, 100, interface, f"{RESSOURCES}/character/idle.png", {55: f"{RESSOURCES}/character/idle.png", 120: f"{RESSOURCES}/character/walking0.png", 190: f"{RESSOURCES}/character/walking1.png", 235: f"{RESSOURCES}/character/walking0.png"}, temp)
    tt = CustomText(0, 0, interface)

    tt.x = interface.window.video_mode.size.x / 2 - tt.texture.size.x / 2
    tt.y = 50

    interface.add_element(MovingBack(0, interface, p))
    interface.add_element(MovingBack(interface.window.video_mode.size.x, interface, p))
    interface.add_gui(tt)

    temp.elements.append(p)
    interface.add_element(p)

    r = Rectangle(0, 500, 925, 100, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(-50, 0, 100, 600, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(500, 0, 100, 600, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    interface.window.set_closable(False)

    return (interface)
