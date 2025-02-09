from CNEngine import *

from .collision_manager import CollisionManager
from .particle import Particle, ParticleSpawner

class Player(Object):
    def __init__(self: object, x: int, y: int, interface: MainInterface, sprite: Texture, animation, collision_manager: CollisionManager = None, max_force_x = 0.6, max_force_y = 1):
        super().__init__(x, y)

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

        self.idle_sprite = get_texture(sprite)
        self.idle_sprite_reverse = get_texture(sprite.split('.png')[0] + "_reverse.png")

        self.size_x = self.idle_sprite.size.x * 2
        self.size_y = self.idle_sprite.size.y * 2

        self.sprite = self.idle_sprite

        self.falling = False

        self.animation_timer = 0
        self.animation = {item: get_texture(animation[item]) for item in animation}
        self.animation_reverse = {item: get_texture(animation[item].split(".png")[0] + "_reverse.png") for item in animation}

        self.spawn_particle_timer = 0

        self.pressed = [False, False, False]

    def update_animation(self, delta_time, running):
        if (running):
            temp = [item for item in self.animation.keys() if item >= self.animation_timer]
            if (not temp):
                self.sprite = self.idle_sprite if self.direction == "right" else self.idle_sprite_reverse
            else:
                self.sprite = self.animation[temp[0]] if self.direction == "right" else self.animation_reverse[temp[0]]
        else:
            self.sprite = self.idle_sprite if self.direction == "right" else self.idle_sprite_reverse

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
            if (not self.falling and not self.jumping):
                self.spawn_particle_timer += delta_time
                if (self.spawn_particle_timer > 30):
                    self.interface.add_gui(ParticleSpawner(self.x + self.size_x / 1.5, self.y + self.size_y / 1.2, self.interface, (1, 0), max_vec_x=0.2, max_vec_y=-0.3, number=3, duration_max=520, density=(0, 0.001), color_set=[(64, 33, 20), (36, 21, 15), (54, 36, 28), (92, 33, 8), (54, 25, 13), (38, 11, 0), (0, 0, 0)]))
                    self.spawn_particle_timer = 0
            self.force_x += delta_time / (100 + (self.max_force_x - self.force_x) * 200)
        else:
            self.force_x -= delta_time / (100 + (self.max_force_x - self.force_x) * 200)

        if (self.force_x < 0):
            self.force_x = 0
        if (self.force_x > self.max_force_x):
            self.force_x = self.max_force_x

        # self.particles.move(*particle_pos)

        # self.particles.update(parent)

        super().update(delta_time)

    def draw(self, screen):
        screen.blit_scaled(self.sprite, Vector2(self.x, self.y), ratios=Vector2(1.8, 1.8))
