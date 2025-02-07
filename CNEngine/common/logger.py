from ..locals import *

from typing import TextIO
from datetime import datetime
import sys

class Logger(object):
    def __init__(self, fp: TextIO = None, ansi: bool = True) -> None:
        self.ansi: bool = ansi
        self.fp: bool = fp

    def write(self, message: str, log_type: str = "info", flush: bool = False) -> None:
        fp: TextIO = self.fp
        if (fp is None):
            fp = sys.stdout
        if (not fp.writable() or fp.closed):
            return
        if (not fp.isatty() or not self.ansi):
            fp.write(f"[{SYMBOLS.get(log_type, '*')}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {message}\n")
        else:
            fp.write(f"{ESCAPE}[40m{ESCAPE}[1m{COLORS.get(log_type, f'{ESCAPE}[34m')}[{SYMBOLS.get(log_type, '*')}]{ESCAPE}[0m{ESCAPE}[40m {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{ESCAPE}[0m | {message}{ESCAPE}[0m\n")

        if (flush):
            fp.flush()