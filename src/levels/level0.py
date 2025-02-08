from CNEngine import *
from hashlib import sha1
from subprocess import Popen, PIPE
from platform import system

class Level0Interface(MainInterface):
    def __init__(self, name, rpc_id = None, icon = None):
        super().__init__(name, rpc_id, icon)

        self.console_out = TextIOLocal()

        self.hash = None
        self.rel_y = 0

        self.size = 14

        self.ctrl = False

        self.texts = []
        self.animation_frame = 0
        self.line_end = True
        self.inputed = ""

    def events(self) -> None:
        super().events()

        key_press = self.window.get_event(EVENT_KEY_DOWN)

        if (key_press and 1073742048 in key_press.key):
            self.ctrl = True

        key_release = self.window.get_event(EVENT_KEY_UP)

        if (key_release and 1073742048 in key_release.key):
            self.ctrl = False

        scroll = self.window.get_event(EVENT_MOUSE_SCROLL)

        if (key_press):
            for key in key_press.key:
                if (key > 31 and key < 127):
                    self.inputed += chr(key)
                if (key == 127 or key == 8):
                    self.inputed = self.inputed[:-1]
                if (key == 13):
                    process = Popen(f"{self.inputed}", executable="C:\\Windows\\System32\\cmd.exe" if system() == "Windows" else "/bin/sh", stderr=PIPE, stdout=PIPE, shell=True)
                    stdout, stderr = process.communicate()

                    self.console_out.file = bytearray(self.console_out.file[:-1] + self.inputed.encode() + b'\n')
                    self.console_out.write(f"{stdout.decode()}{stderr.decode()}\n".replace('\r', ''))
                    self.console_out.write(f"(~/.repos/Game-Jam)-$ \n")
                    self.inputed = ""

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

def build_level0():
    interface: MainInterface = Level0Interface("Terminal emulator", icon=f"{RESSOURCES}/icons/terminal.png")

    interface.console_out.write(f"(~/.repos/Game-Jam)-$ {'./game.exe' if system() == 'Windows' else './game.out'}\n")
    interface.console_out.write("Segmentation fault (core dump)\n")
    interface.console_out.write("(~/.repos/Game-Jam)-$ \n")
    interface.console_out.flush()

    return (interface)
