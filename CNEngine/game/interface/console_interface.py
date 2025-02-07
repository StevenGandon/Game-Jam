from ...interface import Interface, Text, get_texture
from ...sdl_wrapper import (
    VideoMode,
    Vector2,

    EVENT_MOUSE_SCROLL,
    EVENT_KEY_UP,
    EVENT_KEY_DOWN,
    WINDOW_POS_CENTER
)
from ...locals import RESSOURCES, CACHED_FONTS

from hashlib import sha1

class TextIOLocal(object):
    def __init__(self, encoding = "utf-8", errors = "strict", maxlines = 9999) -> None:
        self.closed: bool = False
        self.buffer: str = ""
        self.encoding = encoding
        self.errors = errors
        self.line_buffering = True
        self.mode = "rw"

        self.maxlines = maxlines

        self.name = "LocalIO"

        self.file = bytearray()

    def detach(self):
        return (None)

    def fileno(self) -> int:
        return (-1)

    def isatty(self) -> bool:
        return (False)

    def readable(self) -> bool:
        return True

    def writable(self) -> bool:
        return True

    def close(self) -> None:
        self.closed = True

    def read(self, size: int = -1) -> str:
        temp = bytes(self.file)
        value = temp.decode(self.encoding, errors=self.errors)

        return value if size == -1 else value[:size]

    def write(self, s: str) -> int:
        self.buffer += s

        if ('\n' in s):
            self.flush()

    def flush(self) -> None:
        self.file.extend(self.buffer.encode(self.encoding, errors=self.errors))
        self.buffer = ""

        temp = bytes(self.file)
        temp = temp.split(b'\n')
        while (len(temp) > self.maxlines):
            temp = temp[1:]

        self.file = bytearray(b'\n'.join(temp))

class ConsoleInterface(Interface):
    def __init__(self, title: str = "Console", fp: TextIOLocal = TextIOLocal(), icon: str = None) -> None:
        super().__init__(title, VideoMode(Vector2(925, 600), Vector2(WINDOW_POS_CENTER, WINDOW_POS_CENTER), 32), get_texture(icon) if icon else get_texture(f"{RESSOURCES}/UI/icon.png"))

        self.console_out = fp

        self.hash = None
        self.rel_y = 0

        self.size = 14

        self.ctrl = False

        self.texts = []

    def events(self) -> None:
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

    def update(self, delta_time) -> None:
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

        return super().update(delta_time)

    def draw(self):
        self.window.clear((0, 0, 0))

        for item in self.texts:
            if (item):
                item.draw(self.window)

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
