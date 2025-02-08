from CNEngine import *
from random import randint, uniform

class Particle(Object):
    def __init__(self: object, x: int, y: int, object_ref: list, color: tuple = (255, 0, 0), vector=(0, 0.01), duration=100, density=(0, 0.006)) -> None:
        self.sprite = Texture(Vector2(1, 1))
        self.sprite.clear(color)

        super().__init__(x, y)

        self.vector = list(vector)
        self.duration = duration
        self.density = list(density)

        self.object_ref = object_ref

    def update(self: object, delta_time) -> None:
        self.x = self.x + self.vector[0] * delta_time
        self.y = self.y + self.vector[1] * delta_time

        self.duration -= delta_time

        if (self.duration <= 0 and self in self.object_ref):
            self.object_ref.pop(self.object_ref.index(self))

        self.vector[1] += self.density[1] * delta_time
        self.vector[0] -= self.density[0] * delta_time

    def draw(self: object, screen) -> None:
        screen.blit_scaled(self.sprite, Vector2(self.x, self.y), ratios=Vector2(4, 4))

class ParticleSpawner(Object):
    def __init__(self: object, x: int, y: int, interface, max_pos = (3, 1), cooldown = 0.1, max_vec_x: int = 0.02, max_vec_y: int = 0.015, color_set = [(230, 206, 25), (212, 150, 17), (212, 127, 17), (212, 108, 17), (212, 43, 17), (212, 79, 17), (212, 118, 17)], duration_min = 10, duration_max = 100, number = 1, density = (0, 0.006), life_time = 100) -> None:
        super().__init__(x, y)

        self.timer = cooldown
        self.cooldown = cooldown

        self.max_pos = max_pos

        self.max_vec = [max_vec_x, max_vec_y]

        self.color_set = color_set
        self.durations = [duration_min, duration_max]

        self.particles = []

        self.density = density

        self.number = number

        self.lifetime = life_time
        self.counter_life_time = 0

        self.interface: Interface = interface

    def update(self, delta_time) -> None:
        self.timer -= delta_time
        self.counter_life_time += delta_time

        if (self.lifetime == -1 or self.counter_life_time < self.lifetime) and (self.timer <= 0):
            for i in range(self.number):
                self.particles.append(Particle(self.x + randint(-self.max_pos[0], self.max_pos[0]), self.y + randint(-self.max_pos[1], self.max_pos[1]), self.particles, color=self.color_set[randint(0, len(self.color_set) - 1)], vector=(uniform(-self.max_vec[0], self.max_vec[0]), uniform(0, self.max_vec[1])), duration=randint(self.durations[0], self.durations[1]), density=self.density))
            self.timer = self.cooldown

        if self.lifetime != -1 and self.counter_life_time >= self.lifetime and not self.particles:
            if (self in self.interface.elements):
                self.interface.elements.pop(self.interface.elements.index(self))
            if (self in self.interface.gui):
                self.interface.gui.pop(self.interface.gui.index(self))

        for item in self.particles:
            item.update(delta_time)
        return super().update(delta_time)

    def draw(self, screen: Window):
        for item in self.particles:
            item.draw(screen)
