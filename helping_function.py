import pygame

from setting import *


class help:
    def __init__(self):
        self.original_tile_pos = []

    def check_collision(bulletx, bullety, size1, enemey_or_player, size2):
        rect1 = pygame.Rect(bulletx, bullety, size1[0], size1[1])
        rect2 = pygame.Rect(
            enemey_or_player.x + 10, enemey_or_player.y, size2[0], size2[1]
        )
        if rect1.colliderect(rect2):
            return True

    def animation_img_arr(image_type_name, image_nature, size, index, len):
        if index >= 0:
            temp = []
            for i in range(len):
                img = pygame.transform.scale(
                    pygame.image.load(f"img/{image_type_name}/{image_nature}/{i}.png"),
                    size,
                )
                temp.append(img)
            return temp

        else:
            temp = []
            for i in range(len):
                img = pygame.transform.scale(
                    pygame.image.load(
                        f"img/{image_type_name}/{image_nature}.png"
                    ).convert(),
                    size,
                )
                temp.append(img)
            return temp

    def draw_items_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 20))
        pygame.draw.rect(screen, (255, 0, 0, 1), (x, y, w, h))

    def draw_character(screen, arr, action, index, flip, x, y):
        screen.blit(
            pygame.transform.flip(arr[action][index], flip, False),
            (x, y),
        )

    # show projection for grenade projectile.......
    def show_projection(
        screen,
        flight_time,
        gravity,
        initialPosX,
        initialPosY,
        flip,
        xVelocity,
        yVelocity,
    ):
        for i in range(0, int(flight_time) + 1):
            Y = initialPosY - (yVelocity * i - (gravity * i * i) / 2)
            if flip:
                X = initialPosX - (xVelocity * i)
            else:
                X = initialPosX + (xVelocity * i)

            pygame.draw.circle(screen, (255, 255, 255), (X, Y), 2)

    def load_level_design(self, arr, size):
        image_items_arr = []
        obj = 0
        enemy_arr = []
        water_arr = []

        for i in range(len(arr)):
            for j in range(len(arr[0])):
                val = int(arr[i][j])
                if val >= 0:
                    if val <= 8 or val == 12:
                        img1 = pygame.transform.scale(
                            pygame.image.load(f"img/tile/{arr[i][j]}.png"),
                            size,
                        )
                        obj = 1
                        image_items_arr.append([img1, size[0] * j, size[1] * i, obj])
                    else:
                        if val == 16:
                            enemy_arr.append([size[1] * i, size[0] * j])
                        elif not (val == 15):
                            img1 = pygame.transform.scale(
                                pygame.image.load(f"img/tile/{arr[i][j]}.png"),
                                size,
                            )

                            obj = 0
                            image_items_arr.append(
                                [img1, size[0] * j, size[1] * i, obj]
                            )
                        if val == 9:
                            water_arr.append([size[0] * j, size[1] * i])

        return [image_items_arr, enemy_arr, water_arr]

    def screen_scroll(
        self,
        Screen_width,
        object_pos_arr,
        heroX,
        right_move_boolean,
        left_move_boolean,
        Enemy,
        enemy_death_pos_arr,
        water_arr,
    ):
        count = 0
        count2 = 0
        count3 = 0
        if len(self.original_tile_pos) == 0:
            for all in object_pos_arr:
                self.original_tile_pos.append(all[1])
        for all in object_pos_arr:
            if heroX.x > Screen_width / 2 and right_move_boolean:
                if object_pos_arr[-1][1] >= Screen_width:
                    heroX.is_forward = True
                    if count < len(Enemy):
                        Enemy[count].x -= 3
                    if count2 < len(enemy_death_pos_arr):
                        enemy_death_pos_arr[count2][0] -= 3
                    if count3 < len(water_arr):
                        water_arr[count2][0] -= 3
                    all[1] -= 3

                else:
                    heroX.is_forward = False

            elif heroX.x < (Screen_width / 2 + 6) and left_move_boolean:
                if object_pos_arr[0][1] <= -3:
                    heroX.backward = True
                    if count < len(Enemy):
                        Enemy[count].x += 3
                    if count2 < len(enemy_death_pos_arr):
                        enemy_death_pos_arr[count2][0] += 3
                    if count3 < len(water_arr):
                        water_arr[count2][0] += 3
                    all[1] += 3

                else:
                    heroX.backward = False
            count += 1
            count2 += 1
            count3 += 1

    def is_collide_object(arr, x, y, size):
        rect1 = pygame.Rect(x, y, size[0], size[1])
        for all in arr:
            if all[3]:
                rect2 = pygame.Rect(all[1], all[2], 40, 40)
                if rect1.colliderect(rect2):
                    return True
