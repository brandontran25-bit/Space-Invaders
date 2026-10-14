import pygame

from spaceship import Spaceship
from laser import Laser

class Level2Spaceship(Spaceship):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__(screen_width, screen_height, offset)
        self.shot_level = 1
        self.powerup_end_time = 0
        self.shooting_unlock_time = pygame.time.get_ticks() + 2000

    def add_laser_powerup(self):
        # Single -> Double -> Triple
        self.shot_level = min(3, self.shot_level + 1)

        # Every pickup refreshes the 3 second timer
        self.powerup_end_time = (pygame.time.get_ticks() + 2000)

    def update_laser_powerup(self):
        if (self.shot_level > 1 and pygame.time.get_ticks() >= self.powerup_end_time):
            self.shot_level = 1

    def shoot(self):
        x = self.rect.centerx
        y = self.rect.centery

        if self.shot_level == 1:
            positions = [(x, y)]

        elif self.shot_level == 2:
            positions = [(x - 10, y), (x + 10, y)]

        else:
            positions = [(x - 16, y), (x, y), (x + 16, y)]

        for position in positions:
            laser = Laser(position, 5, self.screen_height)
            self.lasers_group.add(laser)

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        current_time = pygame.time.get_ticks()
        shooting_locked = current_time < self.shooting_unlock_time

        if keys[pygame.K_SPACE] and self.laser_ready and not shooting_locked:
            self.laser_ready = False
            self.shoot()
            self.laser_time = current_time
            self.laser_sound.play()


    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()
        self.update_laser_powerup()