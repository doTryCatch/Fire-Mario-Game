import pygame

from helping_function import *


class bullet:
    def __init__(self, screen, x, y, flip):
        self.screen = screen
        self.bullX = x
        self.bullY = y
        self.flip = flip
        self.is_hit = False
        self.is_Collide = False
        self.speed = 5
        self.img_size = (10, 10)
        self.img = help.animation_img_arr("icons", "bullet", self.img_size, -1, 1)[0]

    def draw_H_Bullet(self, Enemy):
        self.screen.blit(
            pygame.transform.flip(self.img, self.flip, False),
            (self.bullX, self.bullY),
        )
        if self.flip:
            self.bullX -= self.speed
        else:
            self.bullX += self.speed
        for all in Enemy:
            if help.check_collision(
                self.bullX, self.bullY, self.img_size, all, all.img_size
            ):
                all.is_hitted = True
                self.is_hit = True  # for hero character

    def draw_E_Bullet(self, hero):
        self.screen.blit(
            pygame.transform.flip(self.img, self.flip, False), (self.bullX, self.bullY)
        )
        if self.flip:
            self.bullX -= self.speed
        else:
            self.bullX += self.speed

        if help.check_collision(
            self.bullX, self.bullY, self.img_size, hero, hero.img_size
        ):
            hero.is_hitted = True
            self.is_hit = True  # for hero character
