from CNEngine import *
from .objects.end_animation import EndAnimation
from .objects.player import Player
from .objects.collision_manager import CollisionManager
from .objects.particle import Particle, ParticleSpawner


from sdl2.sdlmixer import Mix_OpenAudio, Mix_LoadWAV, Mix_PlayChannel, Mix_Playing, Mix_CloseAudio, MIX_DEFAULT_FORMAT
from sdl2.ext.compat import byteify


class MissingTexture(Object):
    def __init__(self, interface, genericobject, sound_activate = True):
        super().__init__(0, 0)

        self.animation: int = 0
        self.animation_reverse = False
        self.interface = interface
        self.texture = get_texture(f"{ROOT}/assets/ressources/UI/error-icon.png")
        self.button = Button(00, 00, 100, 100, self.click_callback)
        self.window = interface.window
        self.booltexture1 = False
        self.genericobject = genericobject

        self.sound_activate = sound_activate

    def update(self, delta_time):
        if (not self.booltexture1):
            self.button.x = self.genericobject.x
            self.button.y = self.genericobject.y
            self.button.update(delta_time)
        self.genericobject.update(delta_time)

    def click_callback(self, v):
        self.booltexture1 = True

        if (self.sound_activate):
            wav = Mix_LoadWAV(byteify(f"{RESSOURCES}/sound/ding.wav", "utf-8"))
            channel = Mix_PlayChannel(-1, wav, 0)

        self.interface.add_gui(ParticleSpawner(v[0], v[1], self.interface, (1, 0), max_vec_x=0.2, max_vec_y=-0.3, number=6, duration_max=520, density=(0, 0.001), color_set=[(255, 0, 251), (115, 0, 113), (23, 0, 23), (140, 24, 140), (72, 7, 115), (181, 0, 163), (0, 0, 0)]))

    def event(self, window) -> None:
        super().event(window)

        if (not self.booltexture1):
            self.button.event(window)
        self.genericobject.event(window)

    def draw(self, screen):
        if (self.booltexture1):
            self.genericobject.draw(screen)
            return True
        else:
            screen.blit(get_texture(f"{ROOT}/assets/ressources/UI/missing.png"), Vector2(self.genericobject.x, self.genericobject.y))
            return False

class CheckEndCondition(Object):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.interface: MainInterface = interface
        self.activated = False

    def update(self, delta_time):
        if (not self.activated and all(map(lambda x: x.booltexture1, filter(lambda x: isinstance(x, MissingTexture), self.interface.elements)))):
            self.activated = True
            self.interface.add_gui(EndAnimation(self.interface))

    def destroy(self):
        Mix_CloseAudio()

        return super().destroy()

def build_level6(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")

    sound_activate = not Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024)

    cm = CollisionManager()

    interface.add_element(CheckEndCondition(interface))
    interface.add_element(Image(0, 0,  get_texture(F"{RESSOURCES}/background-infinite.png")))
    interface.add_element(MissingTexture(interface, Text(200, 50, "Welcome", 34), sound_activate))
    interface.add_element(MissingTexture(interface, Text(400, 50, "to", 34), sound_activate))
    interface.add_element(MissingTexture(interface, Text(500, 50, "the", 34), sound_activate))
    interface.add_element(MissingTexture(interface, Text(620, 50, "Game", 34), sound_activate))
    interface.add_element(MissingTexture(interface, Player(450, 100, interface, f"{RESSOURCES}/character/idle.png", {55: f"{RESSOURCES}/character/idle.png", 120: f"{RESSOURCES}/character/walking0.png", 190: f"{RESSOURCES}/character/walking1.png", 235: f"{RESSOURCES}/character/walking0.png"}, cm)))

    cm.elements.append(Rectangle(0, 500, 925, 100, (0, 0, 0, 0)))
    cm.elements.append(Rectangle(0, 0, 100, 600, (0, 0, 0, 0)))
    cm.elements.append(Rectangle(825, 0, 100, 600, (0, 0, 0, 0)))

    for item in cm.elements:
        interface.add_element(item)

    interface.show_error_window("NULL POINTER Exception cannot read address 0x00000000")
    interface.show_error_window("Memory violation cannot write address 0x00000030")
    interface.show_error_window("Failed to load file 'assets/game.pkg'")
    interface.show_error_window("Memory error, malloc() of size 0xffffffffffffffffdd failed, out of memory")
    interface.show_error_window("Missing game texture registry 'kgofjfezf.png'")

    interface.window.set_closable(False)

    return (interface)