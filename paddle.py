import pygame

BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, widht, height):
        super().__init__()

        self.image = pygame.Surface([widht, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, widht, height])

        self.rect = self.image.get_rect()

# =================================================================
    def moveLeft(self, pixels):
        self.rect.x -= pixels 
        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 680:
            self.rect.x = 680