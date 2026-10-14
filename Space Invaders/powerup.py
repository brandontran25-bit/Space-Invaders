import pygame

YELLOW = (243, 216, 63)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, position, power_type, screen_height):
        super().__init__()
        self.power_type = power_type
        self.screen_height = screen_height
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        self.speed = 2
        if self.power_type == "laser":
            pygame.draw.line(self.image, YELLOW, (8, 22), (8, 6), 3)
            pygame.draw.line(self.image, YELLOW, (15, 22), (15, 4), 3)
            pygame.draw.line(self.image, YELLOW, (22, 22), (22, 6), 3)

        elif self.power_type == "shield":
            pygame.draw.ellipse(self.image, YELLOW, (3, 5, 24, 20), 3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()