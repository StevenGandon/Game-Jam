from CNEngine import *

class InfiniteLoadingScreen(MainInterface):
    def __init__(self, name, rpc_id=None, icon=None):
        super().__init__(name, rpc_id, icon)

        self.animation_frame = 0
        self.indicators = ["|", "/", "-", "\\"]
        self.indicator_index = 0
        self.size = 20

    def events(self) -> None:
        super().events()

        key_press = self.window.get_event(EVENT_KEY_DOWN)
        if key_press and key_press.key == 1073741886:
            self.destroy()

    def update(self) -> None:
        super().update()

        self.animation_frame += self.delta_time

        if self.animation_frame >= 0.3:
            self.animation_frame = 0
            self.indicator_index = (self.indicator_index + 1) % len(self.indicators)

    def draw(self):
        self.window.clear((0, 0, 0))

        full_text = f"Loading {self.indicators[self.indicator_index]}"

        window_width = self.window.video_mode.size.x
        window_height = self.window.video_mode.size.y
        x = window_width // 2 - (len(full_text) * self.size) // 4
        y = window_height // 2

        text_obj = Text(x, y, full_text, self.size,
                        font=f"{RESSOURCES}/font/ConsolaMono-Book.ttf")
        text_obj.draw(self.window)

        all_windows_draw()

    def destroy(self) -> None:
        for item in tuple(CACHED_FONTS.keys()):
            if "ConsolaMono-Book.ttf" in item:
                CACHED_FONTS[item].close()
                del CACHED_FONTS[item]
        super().destroy()

def build_level2():
    interface: MainInterface = InfiniteLoadingScreen(
        "Infinite Loading Screen",
        icon=f"{RESSOURCES}/icons/loading.png"
    )
    return interface
