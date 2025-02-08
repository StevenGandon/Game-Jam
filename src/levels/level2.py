from CNEngine import *
from .objects.start_animation import StartAnimation

class InfiniteLoadingScreen(Loader):
    def __init__(self, interface):
        super().__init__(0, 0)

        self.interface = interface
        self.animation_frame = 0
        self.indicators = ["|", "/", "-", "\\"]
        self.indicator_index = 0
        self.size = 20

    def event(self, window) -> None:
        super().event(window)

        key_press = window.get_event(EVENT_KEY_DOWN)
        if key_press and 1073741886 in key_press.key:
            self.interface.force_stopped = True

    def update(self, delta_time) -> None:
        self.animation_frame += delta_time

        if self.animation_frame >= 0.3:
            self.animation_frame = 0
            self.indicator_index = (self.indicator_index + 1) % len(self.indicators)

    def draw(self, screen):
        screen.clear((0, 0, 0))

        full_text = f"Loading {self.indicators[self.indicator_index]}"

        window_width = screen.video_mode.size.x
        window_height = screen.video_mode.size.y
        x = window_width // 2 - (len(full_text) * self.size) // 4
        y = window_height // 2

        text_obj = Text(x, y, full_text, self.size,
                        font=f"{RESSOURCES}/font/ConsolaMono-Book.ttf")
        text_obj.draw(screen)

        all_windows_draw()

    def destroy(self) -> None:
        for item in tuple(CACHED_FONTS.keys()):
            if "ConsolaMono-Book.ttf" in item:
                CACHED_FONTS[item].close()
                del CACHED_FONTS[item]
        super().destroy()

def build_level2(interface = None):
    if (not interface):
        interface: MainInterface = MainInterface("Game")
    interface.add_element(InfiniteLoadingScreen(interface))

    interface.add_gui(StartAnimation(interface))

    interface.window.set_closable(False)
    return interface
