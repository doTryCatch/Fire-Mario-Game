import csv
import pygame
from pygame.locals import *

pygame.mixer.init()
Screen_width = 600
Screen_height = 600
player_size = 20
game_sound = {
    "grenade": pygame.mixer.Sound("audio/grenade.wav"),
    "background_music": pygame.mixer.Sound("sound/bg-sound.mp3"),
    "shot": pygame.mixer.Sound("sound/shot.mp3"),
    "jump": pygame.mixer.Sound("sound/jump.wav"),
    "get-item": pygame.mixer.Sound("sound/get-item.mp3"),
    "game-over": pygame.mixer.Sound("sound/game-over.mp3"),
}
levelMap = []
with open(f"level/level1_data.csv", mode="r") as file:
    csv_file = csv.reader(file)
    for all in csv_file:
        levelMap.append(all)
total_game_screen_width = player_size * len(levelMap[0])
