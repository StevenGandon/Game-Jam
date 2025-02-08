from CNEngine import *

class EndAnimation(Object):
    def __init__(self: object, interface: MainInterface):
        super().__init__(0, 0)

        self.interface = interface

        self.top_rect = Rectangle(0, 0, interface.window.video_mode.size.x, 0, (0, 0, 0))
        self.bottom_rect = Rectangle(0, interface.window.video_mode.size.y, interface.window.video_mode.size.x, 0, (0, 0, 0))

        self.boost = 0.1

    def event(self, window: Window):
        pass

    def update(self, delta_time: int):
        if (self.top_rect.size_y + self.bottom_rect.size_y < self.interface.window.video_mode.size.y):
            self.top_rect.size_y += delta_time * self.boost
            self.bottom_rect.y -= delta_time * self.boost
            self.bottom_rect.size_y += delta_time * self.boost
        else:
            self.interface.force_stopped = True

        self.boost += delta_time / 3000.0

        self.top_rect.update(delta_time)
        self.bottom_rect.update(delta_time)

    def draw(self, screen):
        self.top_rect.draw(screen)
        self.bottom_rect.draw(screen)
