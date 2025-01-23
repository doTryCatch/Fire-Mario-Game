import pygame, sys

# from pygame.locals import *
import random
from setting import *
from player import *
from bullet import *
from enemy import *
from game_items import *
from helping_function import *

pygame.init()
game_over = False
enemy_death_Pos = []
tile_size = (40, 38)
player_size = (40, 38)
Enemy = []
Help = help()
screen = pygame.display.set_mode((Screen_width, Screen_height))
clock = pygame.time.Clock()


grenade_item = game_items(screen, "grenade_box")
ammo_item = game_items(screen, "ammo_box")
health_item = game_items(screen, "health_box")
# player weapon and other needed items
items = [
    [grenade_item, ammo_item, health_item],
    ["grenade_item", "ammo_item", "health_item"],
]
# loading the tiles in for game environment
tiles = Help.load_level_design(levelMap, tile_size)
Hero = player(screen, 200, 200, "player")
for all in tiles[1]:
    Enemy.append(enemy(all[1], all[0]))
# text display in the window
font1 = pygame.font.SysFont("freesanbold.ttf", 50)


# Render the texts that you want to display
text1 = font1.render("GAME OVER 🤪🥴", True, (0, 0, 0))


# create a rectangular object for the
# text surface object
textRect1 = text1.get_rect()


# setting center for the first text
textRect1.center = (Screen_width / 2, Screen_height / 2)

# some variables
relax_time = 35
player_down = 35
up = False
right = False
left = False
ctrl = False
F_key = False
dx = Hero.speed
while True:
    for event in pygame.event.get():  # to render all event from pygame..
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # kyboard listner for keydown
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_f:
                F_key = True
            if event.key == pygame.K_LCTRL:
                ctrl = True
        if event.type == pygame.KEYUP:  # kyboard listner for keyup
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_f:
                F_key = False
            if event.key == pygame.K_LCTRL:
                ctrl = False
    #  game start view
    screen.fill((80, 150, 180))
    for all in tiles[0]:
        screen.blit(all[0], (all[1], all[2]))
    if left:
        dx = -Hero.speed
    else:
        dx = Hero.speed
    # screen scroll on player move...
    if not help.is_collide_object(tiles[0], Hero.x + dx, Hero.y, Hero.img_size):
        if right or left:
            Help.screen_scroll(
                Screen_width,
                tiles[0],
                Hero,
                right,
                left,
                Enemy,
                enemy_death_Pos,
                tiles[2],
            )
        # Help.screen_scroll(Screen_width, tiles[1], Hero, right, left)

    # games tiles[0] and blocks and game items
    for all in enemy_death_Pos:
        items[0][all[2]].draw_item(all[0], all[1])
        if help.check_collision(all[0], all[1], (25, 25), Hero, Hero.img_size):
            game_sound["get-item"].play()
            Hero.gain_items(f"{items[1][all[2]]}")
            enemy_death_Pos.remove(
                all
            )  # removing all class of each enemy from the list after thier death
    # load all enemy charater from tiles[1]

    # hero character
    if up:
        game_sound["jump"].play()

    if F_key:
        game_sound["shot"].play()

    # else:

    # pygame.mixer.music.pause()
    if not game_over:
        if Hero.hero_alive:
            Hero.posUpdate(up, left, right, ctrl, F_key, Enemy, tiles[0])
            Hero.DrawPlayer()
            Hero.check_alive(tiles[2])
            Hero.draw_items(screen)

        else:
            if player_down == 0:
                player_down = 35
                game_over = True

            else:
                game_sound["game-over"].play()
                Hero.DrawPlayer()
                Hero.draw_items(screen)
                player_down -= 1
    else:
        screen.blit(text1, textRect1)

    # enemy character
    # print(Enemy[0].x)
    for all in Enemy:
        all.DrawEnemy(screen)
        all.enemy_attack(screen, Hero, bullet, tiles[0])
        all.update(screen)

        # if enemy is killed by hero then deleting that particular class from the enemy array
        if not all.alive:
            if relax_time == 0:
                relax_time = 35
                enemy_death_Pos.append([all.x, all.y, int(random.uniform(0, 3))])
                Enemy.remove(all)

            else:
                relax_time -= 1

    # update is to update the fram do make animation possible..
    pygame.display.update()
    clock.tick(60)  # here 60 is the frequency of the update frmae..
