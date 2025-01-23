import pygame
from setting import *
from helping_function import *
import math, random


class enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flip = False
        self.dir = 1
        self.bull_is_collide = False
        self.counter = 0
        self.index = 0
        self.fire = 0
        self.fire_range = 150
        self.Bullet_arr = []
        self.img_size = (40, 40)
        self.angle = math.pi / 2
        self.playerImg_coll = []
        self.action = 0
        self.speed = 1
        self.update_need = False
        self.animation_time = 5
        self.dx = 0
        self.health = 100
        self.lossHealth_per_bullet = 50
        self.is_hitted = False
        self.alive = True
        self.not_attacking = True
        self.relax_time = 40
        self.pause_time = 100
        self.relax = False
        self.playerImg_coll.append(
            help.animation_img_arr("enemy", "Idle", self.img_size, 0, 5)
        )
        self.playerImg_coll.append(
            help.animation_img_arr("enemy", "Run", self.img_size, 0, 5)
        )
        self.playerImg_coll.append(
            help.animation_img_arr("enemy", "Death", self.img_size, 0, 7)
        )

    def animation_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.counter = 0

    def animation(self):
        if self.counter == self.animation_time:
            self.index += 1
            self.counter = 0
        if self.index == len(self.playerImg_coll[self.action]):
            self.index = 0
        self.counter += 1

    def DrawEnemy(self, screen):
        screen.blit(
            pygame.transform.flip(
                self.playerImg_coll[self.action][self.index], self.flip, False
            ),
            (self.x, self.y),
        )
        self.animation()

    # enemy movement
    def update(self, screen):
        if self.health == 0:
            self.animation_action(2)
            self.alive = False
        if self.alive:
            if self.is_hitted:
                self.health -= self.lossHealth_per_bullet

            if random.randint(0, 200) == 1 and self.relax == False:
                self.relax = True
                self.pause_time = 50
                self.dx = 0
                self.animation_action(0)

            if not self.relax:
                self.animation_action(1)
                if math.sin(self.angle) < 0:
                    self.flip = True
                    self.dx = -self.speed
                    self.dir = 1

                else:
                    self.flip = False
                    self.dx = self.speed
                    self.dir = 0

                self.angle += 0.05
            else:
                self.pause_time -= 1
                if self.pause_time <= 0:
                    self.relax = False

            self.is_hitted = False

        if self.not_attacking and self.alive:
            self.x += self.dx

    def scroll_with_screen(self, Screen_width, heroX, right_boolean, left_boolean):
        if heroX.x > Screen_width / 2 and right_boolean:
            self.x -= 3

        elif heroX.x < (Screen_width / 2 + 6) and heroX.is_forward and left_boolean:
            if heroX.is_forward:
                self.x += 3

    def enemy_attack(self, screen, hero, Enemy_bullet, arr):
        if help.check_collision(
            self.x - self.fire_range * self.dir + 20,
            self.y + 5,
            (self.fire_range, 20),
            hero,
            hero.img_size,
        ):
            self.not_attacking = False
            if hero.x < self.x:
                self.flip = True
                self.dir = -1
            else:
                self.flip = False
                self.dir = 0
            if self.fire == 0:
                self.Bullet_arr.append(Enemy_bullet(screen, self.x, self.y, self.flip))
            self.fire = 1
        else:
            self.not_attacking = True
            self.fire = 0

            if len(self.Bullet_arr) > 0:
                for bull in self.Bullet_arr:
                    bull.draw_E_Bullet(hero)
                if (
                    bull.bullX > Screen_width
                    or bull.bullX < 0
                    or bull.is_hit
                    or help.is_collide_object(
                        arr, bull.bullX, bull.bullY, bull.img_size
                    )
                ):
                    self.Bullet_arr.remove(bull)
