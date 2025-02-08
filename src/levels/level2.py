import math
import colorsys

from CNEngine import *
from .objects.start_animation import StartAnimation

class InfiniteLoadingScreen(Loader):
    def __init__(self, interface):
        super().__init__(0, 0)
        self.interface = interface

        self.size = 40

        self.hue = 0
        self.angle = 0

    def event(self, window) -> None:
        super().event(window)
        key_press = window.get_event(EVENT_KEY_DOWN)
        if key_press:
            if 27 in key_press.key or 1073741886 in key_press.key:
                self.interface.force_stopped = True

    def update(self, delta_time) -> None:
        self.angle += (0.4 * delta_time) % 361
        self.hue = (self.hue + (delta_time * 0.1)) % 361

    def draw(self, screen):
        r_f, g_f, b_f = colorsys.hsv_to_rgb(self.hue / 360.0, 0.5, 0.5)
        r, g, b = int(r_f * 255), int(g_f * 255), int(b_f * 255)
        screen.clear((r, g, b))

        window_width = screen.video_mode.size.x
        window_height = screen.video_mode.size.y

        loading_text = "Loading"
        text_width = len(loading_text) * (self.size // 2)
        margin = 10
        circle_radius = self.size // 2
        text_x = window_width // 2 - text_width // 2
        text_y = window_height // 2 - self.size - margin
        text_obj = Text(
            text_x, text_y,
            loading_text,
            self.size,
            color=(255, 255, 255),
            font=f"{RESSOURCES}/font/ConsolaMono-Book.ttf"
        )
        text_obj.draw(screen)

        circle_center_x = window_width // 2
        circle_center_y = text_y + self.size + margin + circle_radius

        screen.draw_circle(
            (circle_center_x, circle_center_y),
            circle_radius,
            color=(255, 255, 255),
            thickness=2
        )
        dot_radius = 4
        dot_x = circle_center_x + int(math.cos(math.radians(self.angle)) * circle_radius)
        dot_y = circle_center_y + int(math.sin(math.radians(self.angle)) * circle_radius)
        screen.draw_circle(
            (dot_x, dot_y),
            dot_radius,
            color=(255, 255, 255),
            thickness=0
        )

    def destroy(self) -> None:
        for item in tuple(CACHED_FONTS.keys()):
            if "ConsolaMono-Book.ttf" in item:
                CACHED_FONTS[item].close()
                del CACHED_FONTS[item]
        super().destroy()


def build_level2(interface=None):
    if not interface:
        interface: MainInterface = MainInterface("Game")

    interface.add_element(InfiniteLoadingScreen(interface))
    interface.add_gui(StartAnimation(interface))

    interface.window.set_closable(False)
    return interface
