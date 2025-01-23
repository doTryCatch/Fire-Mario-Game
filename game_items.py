import pygame


class game_items:
    def __init__(self, screen, img_name):
        self.img_name = img_name
        self.screen = screen
        self.img_size = (25, 25)

        self.img = pygame.transform.scale(
            pygame.image.load(f"img/icons/{self.img_name}.png"),
            self.img_size,
        )

    def draw_item(self, x, y):
        self.screen.blit(self.img, (x, y))
