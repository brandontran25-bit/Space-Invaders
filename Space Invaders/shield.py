import pygame

YELLOW = (243, 216, 63)

class Shield(pygame.sprite.Sprite):
    def __init__(self, spaceship):
        super().__init__()
        self.spaceship = spaceship
        self.width = 120
        self.height = 85
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.spaceship.rect.center)
        self.duration = 1400
        self.cooldown = 4500
        self.active = False
        self.activation_time = 0
        self.last_used = -self.cooldown
        # Shield power-ups are stored here
        self.bonus_charges = 0

    def activate(self):
        current_time = pygame.time.get_ticks()
        if self.active:
            return
        # Normal rechargeable shield
        if current_time - self.last_used >= self.cooldown:
            self.active = True
            self.activation_time = current_time
            self.last_used = current_time

        # Use collected shield power-up
        elif self.bonus_charges > 0:
            self.bonus_charges -= 1
            self.active = True
            self.activation_time = current_time

    def add_bonus_charge(self):
        # Maximum of 3 stored shields
        self.bonus_charges = min(3, self.bonus_charges + 1)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.rect.center = self.spaceship.rect.center
        if (self.active and current_time - self.activation_time >= self.duration):
            self.active = False
        self.draw_shield()

    def draw_shield(self):
        self.image.fill((0, 0, 0, 0))
        if self.active:
            pygame.draw.ellipse(self.image, YELLOW, (4, 4, self.width - 8, self.height - 8), 3)
            pygame.draw.ellipse(self.image, YELLOW, (12, 10, self.width - 24, self.height - 20), 1)

    def is_ready(self):
        current_time = pygame.time.get_ticks()
        return (not self.active and current_time - self.last_used >= self.cooldown)

    def cooldown_remaining(self):
        current_time = pygame.time.get_ticks()
        remaining = self.cooldown - (current_time - self.last_used)
        return max(0, remaining)