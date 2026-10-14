import pygame
import random
import math

from game import Game
from alien import Alien
from laser import Laser
from shield import Shield
from powerup import PowerUp
from level2_spaceship import Level2Spaceship


class Level2Game(Game):
    def __init__(self, screen_width, screen_height, offset, score=0, lives=3, highscore=0):
        self.wave = 1
        super().__init__(screen_width, screen_height, offset)
        self.score = score
        self.lives = lives
        self.highscore = max(self.highscore, highscore)
        self.spaceship_group.empty()
        self.spaceship_group.add(Level2Spaceship(screen_width, screen_height, offset))
        self.shield = Shield(self.spaceship_group.sprite)
        self.shield_group = pygame.sprite.GroupSingle(self.shield)
        self.powerups_group = pygame.sprite.Group()
        self.normal_speed = 1.2
        self.formation_offset = 0
        self.barrage_warning = False
        self.barrage_active = False
        self.warning_start = 0
        self.barrage_start = 0
        self.warning_duration = 1300
        self.barrage_duration = 1200
        self.next_barrage = (pygame.time.get_ticks() + random.randint(8000, 12000))
        self.wave_transition = False
        self.wave_transition_time = 0
        self.level_complete = False
        self.wave_popup = True
        self.wave_popup_start = pygame.time.get_ticks()
        self.wave_popup_duration = 1500
        self.aliens_group.empty()

    def create_obstacles(self):
        return []

    def create_aliens(self):
        self.formation_offset = 0
        for row in range(4):

            for column in range(10):
                x = 85 + column * 59
                y = 125 + row * 60

                if row == 0:
                    alien_type = 4
                elif row == 1:
                    alien_type = 3
                elif row == 2:
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.offset / 2, y)
                alien.home_x = float(alien.rect.x)
                alien.home_y = float(alien.rect.y)

                if column % 2 == 0:
                    alien.zigzag_direction = 1
                else:
                    alien.zigzag_direction = -1
                
                alien.phase = random.uniform(0, math.pi * 2)
                self.aliens_group.add(alien)

    def move_aliens(self):
        if (self.barrage_warning or self.barrage_active):
            self.move_barrage_aliens()
        else:
            self.move_normal_aliens()

    def move_normal_aliens(self):
        speed = (self.normal_speed + (self.wave - 1) * 0.12)
        self.formation_offset += (speed * self.aliens_direction)
        hit_edge = False

        for alien in self.aliens_group:
            alien.rect.x = int(alien.home_x + self.formation_offset)
            alien.rect.y = int(alien.home_y)
            if (alien.rect.right >= self.screen_width + self.offset / 2):
                hit_edge = True
            elif (alien.rect.left <= self.offset / 2):
                hit_edge = True
        
        if hit_edge:
            self.aliens_direction *= -1
            for alien in self.aliens_group:
                alien.home_y += 3

    def move_barrage_aliens(self):
        current_time = pygame.time.get_ticks()
        left_boundary = int(self.offset/2)
        right_boundary = int(self.screen_width + self.offset/2)

        for alien in self.aliens_group:
            x_wave = math.sin(current_time * 0.006 + alien.phase) * 35
            y_wave = math.sin(current_time * 0.008 + alien.phase) * 10
            new_x = int(alien.home_x + self.formation_offset + (x_wave * alien.zigzag_direction))
            new_x = max(left_boundary, min(new_x, right_boundary - alien.rect.width))
            alien.rect.x = new_x
            alien.rect.y = int(alien.home_y + y_wave)

    def alien_shoot_laser(self):
        if (self.barrage_warning or self.barrage_active):
            return
        aliens = self.aliens_group.sprites()
        if aliens:
            alien = random.choice(aliens)
            laser = Laser(alien.rect.center, -7, self.screen_height)
            self.alien_lasers_group.add(laser)

    def fire_barrage(self):
        aliens = sorted(self.aliens_group.sprites(), key=lambda alien: alien.rect.centerx)
        if not aliens:
            return
        laser_count = min(12, len(aliens))
        step = max(1, len(aliens) // laser_count)
        shooters = aliens[::step]
        shooters = shooters[:laser_count]
        for alien in shooters:
            laser = Laser(alien.rect.center, -9, self.screen_height)
            self.alien_lasers_group.add(laser)

    def update_barrage(self):
        current_time = pygame.time.get_ticks()
        if (not self.barrage_warning and not self.barrage_active and current_time >= self.next_barrage):
            self.barrage_warning = True
            self.warning_start = current_time

        if self.barrage_warning:
            if (current_time - self.warning_start >= self.warning_duration):
                self.barrage_warning = False
                self.barrage_active = True
                self.barrage_start = current_time
                self.fire_barrage()

        if self.barrage_active:
            if (current_time - self.barrage_start >= self.barrage_duration):
                self.barrage_active = False
                for alien in self.aliens_group:
                    alien.rect.x = int(alien.home_x + self.formation_offset)
                    alien.rect.y = int(alien.home_y)
                self.next_barrage = (current_time + random.randint(8000, 12000))

    def maybe_drop_powerup(self, position):
        if random.random() <= 0.05:
            power_type = random.choices(["laser", "shield"], weights=[70, 30])[0]
            powerup = PowerUp(position, power_type, self.screen_height)
            self.powerups_group.add(powerup)

    def collect_powerups(self):
        collected = (pygame.sprite.spritecollide(self.spaceship_group.sprite, self.powerups_group, True))
        for powerup in collected:
            if powerup.power_type == "laser":
                self.spaceship_group.sprite.add_laser_powerup()
            elif powerup.power_type == "shield":
                self.shield.add_bonus_charge()

    def activate_shield(self):
        self.shield.activate()

    def update_shield(self):
        self.shield_group.update()

    def check_for_collisions(self):
        for laser in list(self.spaceship_group.sprite.lasers_group):
            aliens_hit = pygame.sprite.spritecollide(laser, self.aliens_group, True)
            if aliens_hit:
                self.explosion_sound.play()
                for alien in aliens_hit:
                    self.score += (alien.type * 100)
                    self.maybe_drop_powerup(alien.rect.center)
                self.check_for_highscore()
                laser.kill()
                continue

            if pygame.sprite.spritecollide(laser, self.mystery_ship_group, True):
                self.score += 500
                self.explosion_sound.play()
                self.check_for_highscore()
                laser.kill()

        for laser in list(self.alien_lasers_group):
            if (self.shield.active and pygame.sprite.spritecollide(laser, self.shield_group, False)):
                laser.kill()
                continue
            if pygame.sprite.spritecollide(laser, self.spaceship_group, False):
                laser.kill()
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
        self.collect_powerups()
        for alien in self.aliens_group:
            if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                self.game_over()

    def update_wave(self):
        current_time = pygame.time.get_ticks()
        if self.wave_popup:
            return
        if (len(self.aliens_group) == 0 and not self.wave_transition):
            if self.wave < 3:
                self.wave_transition = True
                self.wave_transition_time = (current_time)
            else:
                self.level_complete = True
        if self.wave_transition:
            if (current_time - self.wave_transition_time >= 1500):
                self.wave += 1
                self.wave_transition = False
                self.wave_popup = True
                self.wave_popup_start = current_time
                self.next_barrage = (current_time + random.randint(7000, 10000))

    def get_shield_status(self):
        if self.shield.active:
            return "ACTIVE"
        if self.shield.is_ready():
            return "READY"
        remaining = (self.shield.cooldown_remaining()/1000)
        return f"{remaining:.1f}s"
    
    def update_wave_popup(self):
        if self.wave_popup:
            current_time = pygame.time.get_ticks()

            if current_time - self.wave_popup_start >= self.wave_popup_duration:
                self.wave_popup = False
                self.create_aliens()