from CNEngine import *

from sys import exit
from traceback import format_exc

import builtins
import sys

def main() -> int:
    interface: MainInterface = MainInterface("Game")


    if (interface.rpc):
        pass
        # interface.rpc.set_status(f"", None, f"","", "", "")

    base_print = builtins.print
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

    interface.destroy()

    builtins.print = base_print

    return (0)

if (__name__ == "__main__"):
    exit(main())