import pygame
import math
from setting import *
from helping_function import *


class Bom:
    def __init__(self, screen, x, y, flip):
        self.screen = screen

        self.bomX = x
        self.bomY = y
        self.flip = flip
        self.speed = 4
        self.gravity = 1.25
        self.intialVelocity = 15
        self.bomPos = 0
        self.counter = 0
        self.index = 0
        self.animation_time = 5
        self.anim_time = 35
        self.exploded = False
        self.Vx = self.intialVelocity * math.cos(45)
        self.Vy = self.intialVelocity * math.sin(45)
        self.time = 2 * self.Vy / self.gravity
        self.explosion_img = []
        self.bom_size = (30, 30)
        self.img_size = (20, 20)
        self.img = pygame.transform.scale(
            pygame.image.load(f"img/icons/grenade.png"),
            self.img_size,
        )

        def image_collection_in_array(len):
            temp = []
            for i in range(len):
                img = pygame.transform.scale(
                    pygame.image.load(f"img/explosion/exp{i+1}.png"),
                    self.bom_size,
                )
                temp.append(img)
            self.explosion_img.append(temp)

        image_collection_in_array(4)

    def explosion_animation(self):
        if self.counter == self.animation_time:
            self.index += 1
            self.counter = 0
        if self.index == len(self.explosion_img[0]):
            self.index = 0
            self.exploded = True
        self.counter += 1
        game_sound["grenade"].play()

    def drawBom_projection(self):
        self.exploded = False
        help.show_projection(
            self.screen,
            self.time,
            self.gravity,
            self.bomX,
            self.bomY,
            self.flip,
            self.Vx,
            self.Vy,
        )

    def throwGrenade(self, screen, arr):
        Y = self.bomY - (
            self.Vy * self.bomPos - (self.gravity * self.bomPos * self.bomPos) / 2
        )

        if self.flip:
            X = self.bomX - (self.Vx * self.bomPos)
        else:
            X = self.bomX + (self.Vx * self.bomPos)

        if not help.is_collide_object(arr, X, Y, self.img_size):
            self.bomPos += 0.5

            # screen.blit(self.img, (X, Y))
            pygame.draw.circle(self.screen, (255, 255, 255), (X, Y), 4)
        else:
            if not self.exploded:
                self.explosion(X, Y)

    def explosion(self, X, Y):
        self.screen.blit(self.explosion_img[0][self.index], (X - 15, Y - 15))
        self.explosion_animation()
        if self.anim_time == 0:
            self.anim_time = 35
            self.exploded = True
        else:
            self.anim_time -= 1
