from CNEngine import *

from .collision_manager import CollisionManager

class Player(Object):
    def __init__(self: object, x: int, y: int, interface: MainInterface, sprite: Texture, animation, collision_manager: CollisionManager = None, max_force_x = 0.6, max_force_y = 1):
        super().__init__(x, y)

        self.size_x = sprite.size.x
        self.size_y = sprite.size.y

        # self.particles = ParticleSpawner(self.draw_x, self.draw_y, self.z)

        self.force_x = 0
        self.force_y = 0
        self.max_force_x = max_force_x
        self.max_force_y = max_force_y
        self.direction = "right"
        self.jumping = False
        self.jump_down = False

        self.interface = interface

        self.collision_manager = collision_manager

        self.idle_sprite = sprite

        self.falling = False

        self.animation_timer = 0
        self.animation = animation

        self.pressed = [False, False, False]

    def update_animation(self, delta_time, running):
        if (running):
            temp = [item for item in self.animation.keys() if item >= self.animation_timer]
            if (not temp):
                self.sprite = self.idle_sprite
            else:
                self.sprite = self.animation[temp[0]]
        else:
            self.sprite = self.idle_sprite

        self.animation_timer += delta_time
        if (self.animation_timer > max(self.animation.keys())):
            self.animation_timer = 0

    def event(self, window: Window):
        key_pressed = window.get_event(EVENT_KEY_DOWN)
        key_realesed = window.get_event(EVENT_KEY_UP)

        if (key_pressed):
            if (32 in key_pressed.key):
                self.pressed[0] = True
            if (113 in key_pressed.key):
                self.pressed[1] = True
            if (100 in key_pressed.key):
                self.pressed[2] = True

        if (key_realesed):
            if (32 in key_realesed.key):
                self.pressed[0] = False
            if (113 in key_realesed.key):
                self.pressed[1] = False
            if (100 in key_realesed.key):
                self.pressed[2] = False


    def update(self, delta_time):
        moving = False

        old_y = self.y
        old_x = self.x

        if (self.pressed[0] and not self.jumping and not self.falling):
            self.jumping = True
            self.force_y = 0
            self.jump_down = False
        if (self.pressed[1]):
            self.direction = "left"
            moving = True
        if (self.pressed[2]):
            self.direction = "right"
            moving = True
        if (self.pressed[2] and self.pressed[1]):
            moving = False

        self.update_animation(delta_time, moving)

        if self.jumping and ((not (self.pressed[0])) or self.force_y >= self.max_force_y):
            self.jump_down = True
        if ((self.pressed[0]) and not self.jump_down and self.jumping):
            self.force_y += delta_time / (100 + (self.max_force_y - self.force_y) * 10)

        if (self.jump_down and self.jumping):
            self.force_y -= delta_time / (100 + (self.max_force_y - self.force_y) * 200)

        if (self.direction == "right"):
            self.x = self.x + self.force_x * delta_time
        else:
            self.x = self.x - self.force_x * delta_time

        self.y = self.y - self.force_y * delta_time

        col = self.collision_manager.check_collision(self)
        if (col[0]):
            for item in col[1]:
                if (old_y + self.size_y <= item.y):
                    self.y = item.y - self.size_y

                    self.force_y = 0
                    self.jumping = False
                    self.jump_down = False
                    self.falling = False
                elif (old_y >= item.y + item.size_y):
                    self.y = item.y + item.size_y
                elif (old_x + self.size_x <= item.x):
                    self.x = item.x - self.size_x
                elif (old_x >= item.x + item.size_x):
                    self.x = item.x + item.size_x
        elif (not self.jumping):
            self.falling = True
            self.force_y -= delta_time / (100 + (self.max_force_y - self.force_y) * 200)

        if (moving):
            self.force_x += delta_time / (100 + (self.max_force_x - self.force_x) * 200)
        else:
            self.force_x -= delta_time / (100 + (self.max_force_x - self.force_x) * 200)

        if (self.force_x < 0):
            self.force_x = 0
        if (self.force_x > self.max_force_x):
            self.force_x = self.max_force_x

        if (self.y > 1500):
            self.interface.force_stopped = True

        # self.particles.move(*particle_pos)

        # self.particles.update(parent)

        super().update(delta_time)

    def draw(self, screen):
        screen.blit(self.sprite, Vector2(self.x, self.y))