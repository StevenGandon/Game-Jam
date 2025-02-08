from CNEngine import *
from .objects.end_animation import EndAnimation

class MissingTexture(Object):
    def __init__(self, interface, genericobject):
        super().__init__(0, 0)

        self.animation: int = 0
        self.animation_reverse = False
        self.interface = interface
        self.texture = get_texture(f"{ROOT}/assets/ressources/UI/error-icon.png")
        self.button = Button(00, 00, 100, 100, self.click_callback)
        self.window = interface.window
        self.booltexture1 = False
        self.genericobject = genericobject

    def update(self, delta_time):
        if (not self.booltexture1):
            self.button.x = self.genericobject.x
            self.button.y = self.genericobject.y
            self.button.update(delta_time)
        self.genericobject.update(delta_time)

    def click_callback(self):
        self.booltexture1 = True

    def event(self, window) -> None:
        super().event(window)
        print("Mouse Down")
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
            


def build_level6(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")
    interface.add_element(CheckEndCondition(interface))
    interface.add_element(MissingTexture(interface, Rectangle(0, 0, 100, 100, (0, 0, 255))))
    interface.add_element(MissingTexture(interface, Rectangle(200, 0, 100, 100, (0, 0, 255))))
    
    interface.window.set_closable(False)

    return (interface)