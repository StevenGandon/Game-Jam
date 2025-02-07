from CNEngine import *
from src import *

from sys import exit
from traceback import format_exc

import builtins
import sys

BASE_PRINT = builtins.print

def load_level(level_builder):
    interface: MainInterface = level_builder()

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

    if (interface.force_stopped):
        interface.destroy()

    builtins.print = BASE_PRINT
    interface.destroy()

    return (interface.force_stopped)

def levels_following():
    load_level(build_level0)
    load_level(build_level0)

def main() -> int:
    levels_following()

    builtins.print = BASE_PRINT

    uninit()

    return (0)

if (__name__ == "__main__"):
    exit(main())