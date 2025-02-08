from CNEngine import *
from .objects.player import Player
from .objects.collision_manager import CollisionManager
from .objects.end_animation import EndAnimation
from .objects.start_animation import StartAnimation
from .objects.particle import ParticleSpawner, Particle

class MovingBackground(Object):
    def __init__(self, interface):
        super().__init__(0, 0)

        # self.animation: int = 0
        # self.animation_reverse = False
        self.interface = interface
        self.background = get_texture(f"{ROOT}/assets/ressources/UI/menu.png")

    # def update(self, delta_time):
    #     self.animation += delta_time / 17 if not self.animation_reverse else -(delta_time / 17)

    #     if (self.animation >= self.background.size.x * 0.90 - self.interface.window.video_mode.size.x):
    #         self.animation_reverse = True
    #     if (self.animation <= 0):
    #         self.animation_reverse = False

    #     if (self.animation > self.background.size.x * 0.90 - self.interface.window.video_mode.size.x):
    #         self.animation = self.background.size.x * 0.90 - self.interface.window.video_mode.size.x
    #     if (self.animation < 0):
    #         self.animation = 0

    def draw(self, screen):
        # screen.blit_scaled(self.background, Vector2(0 - self.animation, 0), from_pos=Vector2(0, self.background.size.y * 0.90 / 5), ratios = Vector2(0.90, 0.90))
        screen.blit(self.background, self.x, self.y)

class ConditionHandler(Object):
    def __init__(self, interface, player):
        super().__init__(0, 0)

        self.interface: MainInterface = interface
        self.player = player
        self.collision_manager = CollisionManager(Rectangle(433, 204, 53, 36, (0, 0, 0, 0)))

        self.activated = False

    def update(self, delta_time):
        if (self.collision_manager.check_collision(self.player)[0] and not self.activated):
            self.activated = True
            self.interface.add_gui(EndAnimation(self.interface))

def build_level1(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")
    interface.add_element(MovingBackground(interface))

    temp = CollisionManager()
    p = Player(565, 389, interface, f"{RESSOURCES}/character/idle.png", {55: f"{RESSOURCES}/character/idle.png", 120: f"{RESSOURCES}/character/walking0.png", 190: f"{RESSOURCES}/character/walking1.png", 235: f"{RESSOURCES}/character/walking0.png"}, temp)


    r = Rectangle(0, 550, 925, 100, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(0, 0, 100, 600, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(825, 0, 100, 600, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(295, 453, 244, 9, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(702, 312, 19, 19, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    r = Rectangle(418, 248, 87, 9, (0, 0, 0, 0))
    temp.elements.append(r)
    interface.add_element(r)

    interface.add_gui(Button(292, 187, 349, 70, lambda v: interface.add_gui(ParticleSpawner(v[0], v[1], interface, (1, 0), max_vec_x=0.2, max_vec_y=-0.3, number=6, duration_max=520, density=(0, 0.001), color_set=[(255, 233, 31), (250, 237, 122), (163, 141, 46), (247, 240, 176), (245, 243, 228), (252, 211, 164), (194, 158, 0)]))))
    interface.add_gui(Button(294, 288, 347, 68, lambda v: interface.add_gui(ParticleSpawner(v[0], v[1], interface, (1, 0), max_vec_x=0.2, max_vec_y=-0.3, number=6, duration_max=520, density=(0, 0.001), color_set=[(255, 233, 31), (250, 237, 122), (163, 141, 46), (247, 240, 176), (245, 243, 228), (252, 211, 164), (194, 158, 0)]))))
    interface.add_gui(Button(295, 388, 244, 74, lambda v: interface.add_gui(ParticleSpawner(v[0], v[1], interface, (1, 0), max_vec_x=0.2, max_vec_y=-0.3, number=6, duration_max=520, density=(0, 0.001), color_set=[(255, 233, 31), (250, 237, 122), (163, 141, 46), (247, 240, 176), (245, 243, 228), (252, 211, 164), (194, 158, 0)]))))
    interface.add_gui(Button(565, 389, 74, 74, lambda v=p: interface.add_element(p)))

    interface.add_element(ConditionHandler(interface, p))
    interface.add_gui(StartAnimation(interface))

    interface.window.set_closable(False)

    return (interface)

