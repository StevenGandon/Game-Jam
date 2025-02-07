from threading import Thread

class ThreadWrapper:
    def __init__(self, function) -> None:
        self._function = function
        self._t = Thread(target=self._run_function)
        self._status = None

    def _run_function(self):
        self._status = self._function()

    def start(self):
        self._t.start()

    def is_alive(self):
        return self._t.is_alive()

    def join(self, time):
        self._t.join(time)

        return self._status