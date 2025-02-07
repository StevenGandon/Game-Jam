from ..locals.window_header import EXISTING_WINDOWS

def all_windows_closes() -> bool:
    return (len(EXISTING_WINDOWS) == 0)

def is_window_closed(win_id) -> None:
    for win in tuple(EXISTING_WINDOWS.values()):
        if (win.id == win_id):
            return (False)
    return (True)

def all_windows_update() -> None:
    for win in tuple(EXISTING_WINDOWS.values()):
        win.update()

def all_windows_draw() -> None:
    for win in tuple(EXISTING_WINDOWS.values()):
        win.draw()
