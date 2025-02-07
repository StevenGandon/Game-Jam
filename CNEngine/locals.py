from os import environ

CACHED_FONTS = {}
CACHED_IMAGE = {}

SYMBOLS: dict = {
    "info": '*',
    "warning": '!',
    "success": '+',
    'error': '-'
}

ESCAPE: str = "\033"

COLORS: dict = {
    "info": f"{ESCAPE}[34m",
    "warning": f"{ESCAPE}[33m",
    "success": f"{ESCAPE}[32m",
    "error": f"{ESCAPE}[31m"
}

ROOT: str = environ.get("GAME_ROOT", "./")
RESSOURCES: str = environ.get("GAME_RESSOURCES", ROOT + '/assets/ressources')