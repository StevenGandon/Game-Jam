from CNEngine import *
from .objects.player import Player
from .objects.collision_manager import CollisionManager
from .objects.end_animation import EndAnimation

class MovingBack(Object):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.animation: int = 0
        self.animation_reverse = False
        self.interface = interface
        self.background = get_texture(f"{ROOT}/assets/ressources/UI/arrow.png")
        self.window = interface.window


    def event(self, window) -> None:
        super().event(window)
        key_press = self.window.get_event(EVENT_KEY_DOWN)

        if key_press and 113 in key_press.key:
            self.interface.add_gui(EndAnimation(self.interface))
            print("left")
        if key_press and 100 in key_press.key:
            self.animation += 10
            if self.animation >= self.background.size.x + 250:
                self.animation = 0 - self.background.size.x - 250
            print("right")


    def draw(self, screen):
        screen.blit(self.background, Vector2(0 - self.animation, 0), from_pos=Vector2(0, self.background.size.y * 0.90 / 5), ratios = Vector2(0.90, 0.90))

def build_level5(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")
    interface.add_element(MovingBack(interface))

    temp = CollisionManager()

    r = Rectangle(0, 400, 1000, 1000, (0, 0, 255))
    temp.elements.append(r)
    interface.add_element(r)

    p = Player(100, 100, interface, f"{RESSOURCES}/character/idle.png", {55: f"{RESSOURCES}/character/idle.png", 120: f"{RESSOURCES}/character/walking0.png", 190: f"{RESSOURCES}/character/walking1.png", 235: f"{RESSOURCES}/character/walking0.png"}, temp)
    temp.elements.append(p)
    interface.add_element(p)

    interface.window.set_closable(False)

    return (interface)
