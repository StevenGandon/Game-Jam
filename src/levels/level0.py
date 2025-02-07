from CNEngine import *
from hashlib import sha1

class Level0Interface(MainInterface):
    def __init__(self, name, rpc_id = None, icon = None):
        super().__init__(name, rpc_id, icon)

        self.console_out = TextIOLocal()

        self.hash = None
        self.rel_y = 0

        self.size = 14

        self.ctrl = False

        self.texts = []

    def events(self) -> None:
        super().events()

        key_press = self.window.get_event(EVENT_KEY_DOWN)

        if (key_press and key_press.key == 1073742048):
            self.ctrl = True

        key_release = self.window.get_event(EVENT_KEY_UP)

        if (key_release and key_release.key == 1073742048):
            self.ctrl = False

        scroll = self.window.get_event(EVENT_MOUSE_SCROLL)

        if (not scroll):
            return

        if (not self.ctrl):
            computed_scroll = scroll.y * 20

            if (self.rel_y + computed_scroll >= 0):
                self.rel_y = 0

                self.hash = None
            else:
                self.rel_y += computed_scroll

                self.hash = None
        else:
            self.size += 1 if scroll.y > 0 else -1

            if (self.size < 1):
                self.size = 1
            self.hash = None

            for item in tuple(CACHED_FONTS.keys()):
                if ("ConsolaMono-Book.ttf" in item):
                    CACHED_FONTS[item].close()
                    del CACHED_FONTS[item]

    def update(self) -> None:
        super().update()

        lines = self.console_out.read()
        computed = sha1(lines.encode(), usedforsecurity=False).hexdigest()

        if (computed != self.hash):
            for item in self.texts:
                if (item):
                    item.destroy()
                    del item

            self.texts.clear()
            self.hash = computed

            for i, item in enumerate(lines.split('\n')):
                if (item):
                    self.texts.append(Text(5, self.rel_y + i * self.size, item, self.size, font=f"{RESSOURCES}/font/ConsolaMono-Book.ttf"))
                else:
                    self.texts.append(None)

    def draw(self):
        self.window.clear((0, 0, 0))

        for item in self.interfaces:
            item.draw()

        for item in self.texts:
            if (item):
                item.draw(self.window)
        all_windows_draw()

    def destroy(self) -> None:
        for item in self.texts:
            if (item):
                item.destroy()

        self.texts.clear()

        for item in tuple(CACHED_FONTS.keys()):
            if ("ConsolaMono-Book.ttf" in item):
                CACHED_FONTS[item].close()
                del CACHED_FONTS[item]

        super().destroy()


def build_level0():
    interface: MainInterface = Level0Interface("Terminal emulator")

    interface.console_out.write("~(/.repos/Game-Jam)-$ ./game.out\n")
    interface.console_out.write("Segmentation fault (core dump)\n")
    interface.console_out.flush()

    return (interface)
