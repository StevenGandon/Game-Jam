from ...rpc import *
from ...interface import *
from ...common import *
from ...locals import *
from ...sdl_wrapper import (
    Clock,
    VideoMode,
    Vector2,

    init,
    uninit,
    get_error,
    has_error,
    is_window_closed,
    all_windows_closes,
    all_windows_draw,
    all_windows_update,
    fetch_events,

    INIT_VIDEO,
    INIT_EVENT,
    INIT_IMG_JPG,
    INIT_IMG_PNG,
    WINDOW_POS_CENTER,
    EXISTING_WINDOWS,

    EVENT_KEY_UP,
    SDLK_F12
)

from .error_interface import ErrorInterface
from .console_interface import ConsoleInterface, TextIOLocal

from signal import signal, SIGINT

class MainInterface(Interface):
    def __init__(self, name: str, rpc_id: str = None, icon: str = None) -> None:
        init(INIT_VIDEO | INIT_EVENT | INIT_IMG_JPG | INIT_IMG_PNG)

        self.settings = Settings()
        self.settings.from_file(f"{ROOT}/assets/settings")

        super().__init__(name, VideoMode(Vector2(self.settings.get_setting("main_interface_width", 925), self.settings.get_setting("main_interface_height", 600)), Vector2(WINDOW_POS_CENTER, WINDOW_POS_CENTER), 32), get_texture((f"{RESSOURCES}/" + self.settings.get_setting("main_interface_icon", "UI/icon.png")) if not icon else icon))

        self.fps = self.settings.get_setting("interface_fps", 60)

        self.logger = Logger(TextIOLocal(maxlines=self.settings.get_setting("logger_max_line", 999)))
        self.clock = Clock()

        self.icon_path: str = icon

        self.delta_time: float = 0

        self.recover = False

        self.interfaces: list = []

        self.rpc = DiscordRPC(rpc_id, self.settings.get_setting("discord_rpc", True))

        signal(SIGINT, self.handle_sigint)

    def __del__(self):
        self.destroy()

    def handle_sigint(self, *args, **kwargs) -> None:
        for item in tuple(EXISTING_WINDOWS.values()):
            item.destroy()

    def add_interface(self, interface: Interface):
        self.interfaces.append(interface)

    def show_console(self) -> None:
        if (any(map(lambda x: isinstance(x, ConsoleInterface), self.interfaces))):
            self.show_error_window(f"Console menu already open.")
            return

        self.add_interface(ConsoleInterface(fp=self.logger.fp, icon=self.icon_path))

    def show_error_window(self, error_message: str) -> None:
        self.add_interface(ErrorInterface(error_message=error_message))

    def events(self) -> None:
        fetch_events()

        super().events()

        if (self.window.check_event(EVENT_KEY_UP) and self.window.get_event(EVENT_KEY_UP).key == SDLK_F12):
            self.show_console()

        for item in self.interfaces:
            item.events()

    def update(self) -> None:
        super().update(self.delta_time)

        for item in self.interfaces:
            item.update(self.delta_time)

        all_windows_update()

        if (any(map(lambda item: is_window_closed(item.window.id), self.interfaces))):
            self.interfaces = [item for item in self.interfaces if not is_window_closed(item.window.id)]

    def draw(self) -> None:
        self.window.clear((0, 0, 0))

        super().draw()

        for item in self.interfaces:
            item.draw()

        all_windows_draw()

    def run(self) -> None:
        events = self.events
        update = self.update
        draw = self.draw
        clock = self.clock

        while (not all_windows_closes()):
            events()
            update()
            draw()
            self.delta_time: float = clock.tick(self.fps)

        if (has_error()):
            while (has_error()):
                self.logger.write(f"SDL_ERROR_STACK: {get_error()}.", "error", flush=True)

    def destroy(self) -> None:
        self.window.destroy()

        self.logger.write(f"Removing caches.", flush=True)
        for item in CACHED_IMAGE:
            CACHED_IMAGE[item].destroy()

        for item in CACHED_FONTS:
            CACHED_FONTS[item].close()

        CACHED_IMAGE.clear()
        CACHED_FONTS.clear()

        for item in self.interfaces:
            item.destroy()

        self.interfaces.clear()

        self.logger.write(f"Stopping RPC.", flush=True)
        self.rpc.stop()

        self.logger.write(f"Uniniting SDL2.", flush=True)
        uninit()
