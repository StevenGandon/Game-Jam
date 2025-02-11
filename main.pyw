import builtins
import sys
import os

from platform import system

if (system() == "Windows"):
    os.environ["PYSDL2_DLL_PATH"] = "./lib"

from CNEngine import *
from src import *

from sys import exit
from traceback import format_exc

from sdl2.sdlmixer import Mix_OpenAudio, Mix_LoadWAV, Mix_PlayChannel, Mix_Playing, Mix_CloseAudio, MIX_DEFAULT_FORMAT
from sdl2.ext.compat import byteify

BASE_PRINT = builtins.print
LAST_WINDOW = None

def load_level(level_builder, rebuild_window=True, clear_datas=True):
    global LAST_WINDOW

    if (LAST_WINDOW):
        for item in LAST_WINDOW.gui:
            item.destroy()
        LAST_WINDOW.gui.clear()
        if (clear_datas):
            for item in LAST_WINDOW.elements:
                item.destroy()
            LAST_WINDOW.elements.clear()
            if (hasattr(LAST_WINDOW, "interfaces")):
                for item in LAST_WINDOW.interfaces:
                    item.destroy()
                LAST_WINDOW.interfaces.clear()
        LAST_WINDOW.force_stopped = False

        if (rebuild_window):
            LAST_WINDOW.destroy()
            LAST_WINDOW = None

    interface: MainInterface = level_builder(None if rebuild_window else LAST_WINDOW)

    if (rebuild_window):
        LAST_WINDOW = interface

    if (interface.rpc):
        pass
        # interface.rpc.set_status(f"", None, f"","", "", "")

    builtins.print = lambda *x: interface.logger.write(''.join(map(str, x)))

    try:
        interface.run()
    except Exception:
        interface.logger.write(f"Uncaught error:\n{format_exc()}", log_type="error", flush=True)
        interface.recover = True
        sys.stdout.write(f"Uncaught error:\n{format_exc()}")

    while (interface.recover):
        interface.recover = False
        try:
            interface.run()
        except Exception as e:
            interface.logger.write(f"Uncaught error:\n{format_exc()}", log_type="error", flush=True)
            interface.recover = True

    builtins.print = BASE_PRINT

    return (interface.force_stopped)

def levels_following():
    load_level(build_level0, rebuild_window = True)
    if (not load_level(build_level1, rebuild_window=True)):
        return
    if (not load_level(build_level2, rebuild_window=False)):
        return
    if (not load_level(build_levelX, rebuild_window=False)):
        return
    if (not load_level(build_level3, rebuild_window=False, clear_datas=False)):
        return
    if not Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024):
        wav = Mix_LoadWAV(byteify(f"{RESSOURCES}/sound/error.wav", "utf-8"))
        channel = Mix_PlayChannel(-1, wav, 0)
    if (not load_level(build_level6, rebuild_window=False)):
        return
    Mix_CloseAudio()
    load_level(build_level5, rebuild_window=False)

    if not Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024):
        wav = Mix_LoadWAV(byteify(f"{RESSOURCES}/sound/spas12.wav", "utf-8"))
        channel = Mix_PlayChannel(-1, wav, 0)
    load_level(build_levelend, rebuild_window=True)
    Mix_CloseAudio()

def main() -> int:
    global LAST_WINDOW

    levels_following()

    if (LAST_WINDOW):
        LAST_WINDOW.destroy()
        LAST_WINDOW = None

    builtins.print = BASE_PRINT

    uninit()

    return (0)

if (__name__ == "__main__"):
    exit(main())