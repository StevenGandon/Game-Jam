from ..sdl_wrapper import Window, Vector2

class Loader(object):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.childs = []

        self.attachement_data = {

        }

    def add_child(self, item):
        self.childs.append(item)

        self.attachement_data[item] = Vector2(item.x, item.y)

    def event(self, window: Window) -> None:
        for item in self.childs:
            item.event(window)

    def update(self, delta_time) -> None:
        for item in self.childs:
            if ((item.x - self.x != self.attachement_data[item].x)):
                item.x = self.x + self.attachement_data[item].x
            if ((item.y - self.y != self.attachement_data[item].y)):
                item.y = self.y + self.attachement_data[item].y

            item.update()

    def draw(self, screen: Window) -> None:
        for item in self.childs:
            item.draw(screen)

    def destroy(self) -> None:
        for item in self.childs:
            item.destroy()

    def __hash__(self) -> int:
        return (id(self))
