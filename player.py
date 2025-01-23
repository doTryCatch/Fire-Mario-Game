from setting import *
from bullet import *
from grinade import *


class player:
    def __init__(self, screen, x, y, char_type):
        self.char_type = char_type
        self.behave = "Idle"
        self.screen = screen
        self.x = x
        self.y = y
        self.Bullet_arr = []
        self.grinage = []
        self.gravity = 2.4
        self.vel = 0
        self.speed = 4
        self.dx = 0
        self.dy = 0
        self.groun_height = 0
        self.max_jump_height = 120
        self.jumped = False
        self.flip = False
        self.dir = 1
        self.action = 0
        self.is_forward = True
        self.backward = True
        self.fire = 0
        self.bomThrow = 0
        self.is_hitted = False
        self.hero_alive = True
        self.hero_grenade_num = 10
        self.hero_ammo_num = 20
        self.hero_health = 100
        self.fall_in_water = False
        self.health_decrease_per_bullet = 20

        self.counter = 0
        self.index = 0
        self.animation_time = 5
        self.playerImg_coll = []
        self.img_size = (40, 40)

        self.playerImg_coll.append(
            help.animation_img_arr(self.char_type, "Idle", self.img_size, 0, 5)
        )
        self.playerImg_coll.append(
            help.animation_img_arr(self.char_type, "Run", self.img_size, 0, 6)
        )
        self.playerImg_coll.append(
            help.animation_img_arr(self.char_type, "Jump", self.img_size, 0, 1)
        )
        self.playerImg_coll.append(
            help.animation_img_arr(self.char_type, "Death", self.img_size, 0, 8)
        )
        # image_collection_in_array(self.char_type, "Run", 6)

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

    def DrawPlayer(self):
        help.draw_character(
            self.screen,
            self.playerImg_coll,
            self.action,
            self.index,
            self.flip,
            self.x,
            self.y,
        )

        self.animation()

    def posUpdate(self, up, left, right, ctrl, F_key, Enemy, obj_arr):
        self.vel = self.gravity

        if help.is_collide_object(
            obj_arr, self.x, self.y + self.gravity, self.img_size
        ):
            self.jumped = False
            self.groun_height = self.y
            self.dy = 0
        else:
            self.dy = self.vel

        # player direction change on key event
        if right or left:
            self.animation_action(1)
        else:
            self.animation_action(0)
        # fire controll
        if ctrl:
            Bom(self.screen, self.x + 24, self.y + 20, self.flip).drawBom_projection()
            if self.bomThrow == 0:
                if self.hero_grenade_num > 0:
                    self.hero_grenade_num -= 1
                self.grinage.append(
                    Bom(self.screen, self.x + 24, self.y + 20, self.flip)
                )
            self.bomThrow = 1

        else:
            self.bomThrow = 0
        if self.hero_grenade_num > 0:
            if len(self.grinage) > 0:
                for bom in self.grinage:
                    bom.throwGrenade(self.screen, obj_arr)
                    if bom.exploded:
                        self.grinage.remove(bom)

        if F_key:
            if self.fire == 0:
                if self.hero_ammo_num > 0:
                    self.hero_ammo_num -= 1
                self.Bullet_arr.append(bullet(self.screen, self.x, self.y, self.flip))
            self.fire = 1
        else:
            self.fire = 0
        if self.hero_ammo_num > 0:
            if len(self.Bullet_arr) > 0:
                for bull in self.Bullet_arr:
                    bull.draw_H_Bullet(Enemy)

                    if (
                        bull.bullX > Screen_width
                        or bull.bullX < 0
                        or bull.is_hit
                        or bull.is_Collide
                    ):
                        self.Bullet_arr.remove(bull)

        # player movement
        if up:
            self.animation_action(2)
            if not self.jumped:
                if (
                    self.groun_height - self.y < self.max_jump_height
                    and self.groun_height - self.y > -5
                ):
                    self.dy = -self.speed
                else:
                    self.jumped = True

            if help.is_collide_object(
                obj_arr, self.x, self.y - self.speed, self.img_size
            ):
                self.dy = 0

        if right:
            self.flip = False
            self.dir = 1
            self.dx = self.speed
            if help.is_collide_object(
                obj_arr, self.x + self.speed, self.y, self.img_size
            ):
                self.dx = 0
            if not (self.is_forward and self.x > (Screen_width / 2) + 5):
                self.x += self.dx

        if left:
            self.flip = True
            self.dir = -1
            self.dx = -self.speed
            if help.is_collide_object(
                obj_arr, self.x - self.speed, self.y, self.img_size
            ):
                self.dx = 0
            if not (self.x < Screen_width / 2 + 6 and self.backward):
                self.x += self.dx

        self.y += self.dy

    def check_alive(self, arr):
        if self.is_hitted and self.hero_health > 0:
            self.hero_health -= self.health_decrease_per_bullet
        self.is_hitted = False
        if self.hero_health == 0:
            self.animation_action(3)
            self.hero_alive = False
        if self.fall_in_water or self.y > Screen_height:
            self.hero_health -= 0.5

        rect1 = pygame.Rect(self.x, self.y, self.img_size[0], self.img_size[1])
        for all in arr:
            rect2 = pygame.Rect(all[0], all[1], 40, 35)
            if rect1.colliderect(rect2):
                print("fall in water")
                self.fall_in_water = True

    def gain_items(self, items_name):
        print(type(items_name), items_name)
        if items_name == "health_item":
            if self.hero_health < 100:
                self.hero_health += 20
        elif items_name == "grenade_item":
            self.hero_grenade_num += 2
        else:
            self.hero_ammo_num += 5

    def draw_items(self, screen):
        help.draw_items_rect(screen, 15, 10, self.hero_health, 20)
        # load image for bullet
        bullet = pygame.transform.scale(
            pygame.image.load(f"img/icons/bullet.png"),
            (10, 10),
        )
        grenade = pygame.transform.scale(
            pygame.image.load(f"img/icons/grenade.png"),
            (10, 10),
        )

        # draw every bullet available
        for i in range(self.hero_ammo_num - 1):
            screen.blit(bullet, (i * 10 + 20, 45))

            # draw grenage
        for i in range(self.hero_grenade_num - 1):
            screen.blit(grenade, (i * 10 + 20, 30))
