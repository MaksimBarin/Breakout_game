import pygame

BLACK = (0, 0, 0)

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, widht, height):
        super().__init__()

        self.image = pygame.Surface([widht, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, widht, height])

        self.rect = self.image.get_rect()