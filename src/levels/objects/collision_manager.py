class CollisionManager(object):
    def __init__(self, *args) -> None:
        self.elements = list(args)

    def check_collision(self, element):
        stored = []
        for item in self.elements:
            if (item != element and element.x < item.x + item.size_x and
    element.x + element.size_x > item.x and
    element.y < item.y + item.size_y and
    element.y + element.size_y > item.y):
                stored.append(item)
        return (False, None) if not stored else (True, stored)