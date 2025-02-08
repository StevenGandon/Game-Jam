from CNEngine import *
from src import *

from sys import exit
from traceback import format_exc

import builtins
import sys

BASE_PRINT = builtins.print
LAST_WINDOW = None

def load_level(level_builder, rebuild_window=True, clear_datas=True):
    global LAST_WINDOW

    if (LAST_WINDOW):
        if (clear_datas):
            LAST_WINDOW.gui.clear()
            LAST_WINDOW.elements.clear()
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
    if (not load_level(build_level3, rebuild_window=False, clear_datas=False)):
        return

def main() -> int:
    global LAST_WINDOW

    levels_following()

    LAST_WINDOW.destroy()
    LAST_WINDOW = None

    builtins.print = BASE_PRINT

    uninit()

    return (0)

if (__name__ == "__main__"):
    exit(main())