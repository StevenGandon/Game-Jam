from CNEngine import *
from .objects.player import Player
from .objects.collision_manager import CollisionManager

class MovingBackground(Object):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.animation: int = 0
        self.animation_reverse = False
        self.interface = interface
        self.background = get_texture(f"{ROOT}/assets/ressources/UI/bg_blured.png")

    def update(self, delta_time):
        self.animation += delta_time / 17 if not self.animation_reverse else -(delta_time / 17)

        if (self.animation >= self.background.size.x * 0.90 - self.interface.window.video_mode.size.x):
            self.animation_reverse = True
        if (self.animation <= 0):
            self.animation_reverse = False

        if (self.animation > self.background.size.x * 0.90 - self.interface.window.video_mode.size.x):
            self.animation = self.background.size.x * 0.90 - self.interface.window.video_mode.size.x
        if (self.animation < 0):
            self.animation = 0

    def draw(self, screen):
        screen.blit(self.background, Vector2(0 - self.animation, 0), from_pos=Vector2(0, self.background.size.y * 0.90 / 5), ratios = Vector2(0.90, 0.90))

def build_level1():
    interface: MainInterface = MainInterface("Game")
    interface.add_element(MovingBackground(interface))

    temp = CollisionManager()

    r = Rectangle(0, 400, 1000, 1000, (0, 0, 255))
    temp.elements.append(r)
    interface.add_element(r)

    p = Player(100, 100, get_texture("aaa"), {55: get_texture("vvv")}, temp)
    temp.elements.append(p)
    interface.add_element(p)

    interface.window.set_closable(False)

    return (interface)

