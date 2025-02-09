from CNEngine import *
from hashlib import sha1
from subprocess import Popen, PIPE
from platform import system
from sdl2 import SDL_MinimizeWindow

class LevelEndInterface(MainInterface):
    def __init__(self, name, rpc_id = None, icon = None):
        super().__init__(name, rpc_id, icon)

        SDL_MinimizeWindow(self.window.window)

        self.console_out = TextIOLocal()

        self.hash = None
        self.rel_y = 0

        self.size = 14

        self.ctrl = False

        self.texts = []
        self.animation_frame = 0
        self.end_animation_frame = 0
        self.line_end = True
        self.inputed = ""

        self.mode_close = False

    def events(self) -> None:
        super().events()

        key_press = self.window.get_event(EVENT_KEY_DOWN)

        if (key_press and 1073742048 in key_press.key):
            self.ctrl = True

        key_release = self.window.get_event(EVENT_KEY_UP)

        if (key_release and 1073742048 in key_release.key):
            self.ctrl = False

        scroll = self.window.get_event(EVENT_MOUSE_SCROLL)

        if (self.window.get_event(EVENT_QUIT) or self.window.get_event(EVENT_CLOSE)):
            self.mode_close = True

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

        self.animation_frame += self.delta_time

        if (self.mode_close):
            if (self.inputed == "Thanks for playing\n"):
             if (self.end_animation_frame > 4096):
                 self.force_stopped = True
            elif (self.end_animation_frame > 255):
                self.inputed += "Thanks for playing\n"[len(self.inputed)]
                self.end_animation_frame = 0
            self.end_animation_frame += self.delta_time

        if (self.animation_frame > 137):
            self.animation_frame = 0
            self.line_end = not self.line_end

        lines = self.console_out.read()
        computed = sha1((lines + f"{self.line_end}{self.inputed}").encode(), usedforsecurity=False).hexdigest()

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

            i = 1
            while i <= len(self.texts) and not self.texts[-i]:
                i += 1
            if (i <= len(self.texts) and self.texts[-i]):
                self.texts[-i].set_text(self.texts[-i].text + self.inputed + ("_" if self.line_end else ""))


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

def build_levelend(last_interface = None):
    interface: MainInterface = LevelEndInterface("Terminal emulator", icon=f"{RESSOURCES}/icons/terminal.png")

    interface.window.set_closable(False)

    interface.console_out.write(f"(~/.repos/Game-Jam)-$ {'./game.exe' if system() == 'Windows' else './game.out'}\n")
    interface.console_out.write("Segmentation fault (core dump)\n")
    interface.console_out.write("(~/.repos/Game-Jam)-$ \n")
    interface.console_out.flush()

    return (interface)
