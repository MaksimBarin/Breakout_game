import pygame
from random import randint

BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, widht, height):
        super().__init__()

        self.image = pygame.Surface([widht, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, widht, height])

        self.velocity = [randint(4, 8), randint(-6, 6)]
        while self.velocity[1] == 0:
            self.velocity[1] = randint(-6, 6)

        self.rect = self.image.get_rect()

# ================================================================
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        # self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-6, 6)
        while self.velocity[1] == 0:
            self.velocity[1] = randint(-6, 6)