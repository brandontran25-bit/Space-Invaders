import math
import os
import random
import pygame
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

YELLOW = (243, 216, 63)
ORANGE = (255, 134, 32)
RED = (230, 43, 47)
DARK_RED = (112, 20, 35)
GREY = (29, 29, 27)

class TitleScreen:
    def __init__(self, surface, font_path="Font/monogram.ttf"):
        self.surface = surface
        self.width, self.height = surface.get_size()
        self.font_path = resource_path(font_path)
        self.time = 0.0
        self.prompt_visible = True

        rng = random.Random(23)
        self.stars = []
        for _ in range(115):
            self.stars.append({"x": rng.randrange(18, self.width - 18), "y": rng.randrange(18, self.height - 18), "speed": rng.uniform(8, 24), "size": rng.choice((1, 1, 1, 2)), "phase": rng.uniform(0, math.tau),})

        self.title_font = self._load_font(96)
        self.prompt_font = self._load_font(30)
        self.info_font = self._load_font(20)
        self.alien_images = {alien_type: self._fit_sprite(pygame.image.load(resource_path(f"Graphics/alien_{alien_type}.png")).convert_alpha(), max_width=48, max_height=36) for alien_type in range(1, 5)}
        self.mystery_image = self._fit_sprite(pygame.image.load(resource_path("Graphics/mystery.png")).convert_alpha(), max_width=48, max_height=36)

    def _load_font(self, size):
        if os.path.isfile(self.font_path):
            return pygame.font.Font(self.font_path, size)
        return pygame.font.SysFont("monospace", size, bold=True)

    @staticmethod
    def _fit_sprite(image, max_width=48, max_height=36):
        original_width, original_height = image.get_size()
        if original_width <= 0 or original_height <= 0:
            return image

        scale = min(max_width / original_width, max_height / original_height)
        size = (max(1, round(original_width * scale)), max(1, round(original_height * scale)))
        return pygame.transform.scale(image, size)

    def update(self, delta_seconds):
        self.time += max(0.0, delta_seconds)

        for star in self.stars:
            star["y"] += star["speed"] * delta_seconds
            if star["y"] >= self.height - 16:
                star["y"] = 12
                star["x"] = random.randrange(18, self.width - 18)

        self.prompt_visible = (int(self.time * 2) % 2 == 0)

    def _draw_logo_line(self, text, center_y, size, max_width):
        logo_font = self._load_font(size)
        main = logo_font.render(text, False, YELLOW)
        if main.get_width() > max_width:
            ratio = max_width / main.get_width()
            main = pygame.transform.scale(main, (max_width, max(1, int(main.get_height() * ratio))))
        x = (self.width - main.get_width()) // 2
        y = int(center_y - main.get_height() // 2)

        dark = logo_font.render(text, False, DARK_RED)
        red = logo_font.render(text, False, RED)
        orange = logo_font.render(text, False, ORANGE)
        if dark.get_size() != main.get_size():
            dark = pygame.transform.scale(dark, main.get_size())
            red = pygame.transform.scale(red, main.get_size())
            orange = pygame.transform.scale(orange, main.get_size())

        for depth in range(12, 3, -2):
            self.surface.blit(dark, (x + 4, y + depth))
        self.surface.blit(red, (x + 2, y + 5))
        self.surface.blit(orange, (x + 1, y + 2))
        self.surface.blit(main, (x, y))

    def draw(self):
        self.surface.fill(GREY)

        for star in self.stars:
            glow = 100 + int(85 * (0.5 + 0.5 * math.sin(self.time * 2.0 + star["phase"])))
            colour = (glow, glow, min(255, glow + 12))
            pygame.draw.rect(self.surface, colour, (int(star["x"]), int(star["y"]), star["size"], star["size"]))

        pygame.draw.rect(self.surface, YELLOW, (10, 10, self.width - 20, self.height - 20), width=2, border_radius=60)

        logo_sway = int(math.sin(self.time * 1.3) * 2)
        self._draw_logo_line("SPACE", 93 + logo_sway, 96, self.width - 120)
        self._draw_logo_line("INVADERS", 178 - logo_sway, 84, self.width - 90)

        formation_shift = math.sin(self.time * 0.85) * 6
        alien_rows = [2, 1, "mystery", 3, 4, 1]
        start_x = 105
        start_y = 250
        column_spacing = 59
        row_spacing = 48

        for row, alien_type in enumerate(alien_rows):
            for column in range(10):
                if alien_type == "mystery":
                    alien_image = self.mystery_image
                else:
                    alien_image = self.alien_images[alien_type]

                x = start_x + column * column_spacing + formation_shift
                y = start_y + row * row_spacing
                y += math.sin(self.time * 1.8 + column * 0.35 + row * 0.25) * 1.5

                alien_rect = alien_image.get_rect()
                alien_rect.center = (int(x + 24), int(y + 24))
                self.surface.blit(alien_image, alien_rect)

        if self.prompt_visible:
            prompt = self.prompt_font.render("PRESS SPACE TO START", False, YELLOW)
            prompt_rect = prompt.get_rect(center=(self.width // 2, 574))
            self.surface.blit(prompt, prompt_rect)
