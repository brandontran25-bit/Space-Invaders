import pygame, sys, random, os
from game import Game
from level2 import Level2Game
from title_screen import TitleScreen

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)
WHITE = (255, 255, 255)

font = pygame.font.Font(resource_path("Font/monogram.ttf"), 40)
small_font = pygame.font.Font(resource_path("Font/monogram.ttf"), 24)
level_1_surface = font.render("LEVEL 01", False, YELLOW)
level_2_surface = font.render("LEVEL 02", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)
show_title = True
title_screen = TitleScreen(screen, "Font/monogram.ttf")

title_start_time = pygame.time.get_ticks()
TITLE_MIN_DISPLAY_MS = 2000
title_has_started = False

current_level = 1

waiting_for_level2 = False

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

while True:
    events = pygame.event.get()
    if show_title:
        delta_seconds = clock.tick(60)/1000.0
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_title = False

        title_screen.update(delta_seconds)
        title_screen.draw()
        pygame.display.flip()
        continue

    #Checking for events
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.run and not waiting_for_level2:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.run and not waiting_for_level2:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game.run and not waiting_for_level2:
                if current_level == 2:
                    game = Level2Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, 0, 3, game.highscore)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1)
                    pygame.time.set_timer(SHOOT_LASER, 450)
                else:
                    game.reset()

        #Start Level 2 when SPACE is pressed
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and waiting_for_level2):
            previous_score = game.score
            previous_lives = game.lives
            previous_highscore = game.highscore

            game = Level2Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET, previous_score, previous_lives, previous_highscore)

            current_level = 2
            waiting_for_level2 = False

            pygame.time.set_timer(SHOOT_LASER, 450)

        #Activate Level 2 shield
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_e and current_level == 2 and game.run and not waiting_for_level2):
            game.activate_shield()

    #Updating
    if game.run and not waiting_for_level2:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()

    if current_level == 2 and game.run and not waiting_for_level2:
        game.powerups_group.update()
        game.update_shield()
        game.update_barrage()
        game.update_wave()
        game.update_wave_popup()

    game.check_for_collisions()

    #Level 1 finished
    if (current_level == 1 and len(game.aliens_group) == 0 and not waiting_for_level2):
        waiting_for_level2 = True

    #Drawing
    screen.fill(GREY)

    #UI
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

    if game.run:
        if current_level == 1:
            screen.blit(level_1_surface, (570, 740))
        else:
            screen.blit(level_2_surface, (570, 740))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 732))
        x += 50

    if current_level == 2:
        #Small shield icon
        pygame.draw.ellipse(screen, YELLOW, (270, 744, 30, 20), 2)

        #Stored shield power-ups
        shield_count = font.render(f"x{game.shield.bonus_charges}", False, YELLOW)

        screen.blit(shield_count, (305, 735))

        #E shield status
        shield_status = font.render(game.get_shield_status(), False, YELLOW)
        screen.blit(shield_status, (370, 735))

    #Incoming barrage warning box
    if current_level == 2 and game.run and game.barrage_warning and not waiting_for_level2:
        warning_box = pygame.Rect(225, 72, 350, 42)
        pygame.draw.rect(screen, GREY, warning_box)
        pygame.draw.rect(screen, YELLOW, warning_box, 3)
        warning_surface = font.render("INCOMING BARRAGE", False, YELLOW)
        screen.blit(warning_surface, warning_surface.get_rect(center=warning_box.center))

        shield_warning_surface = (small_font.render("PRESS E TO DEPLOY SHIELD", False, YELLOW))
        screen.blit(shield_warning_surface, shield_warning_surface.get_rect(center=(400, 130)))

    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (625, 40, 50, 50))

    #Wave popup
    if current_level == 2 and game.run and game.wave_popup:
        wave_box = pygame.Rect(250, 280, 300, 120)
        pygame.draw.rect(screen, GREY, wave_box)
        pygame.draw.rect(screen, YELLOW, wave_box, 3)
        wave_surface = font.render(f"WAVE {game.wave}", False, YELLOW)
        screen.blit(wave_surface, wave_surface.get_rect(center=wave_box.center))

    game.spaceship_group.draw(screen)
    if current_level == 2:
        game.shield_group.draw(screen)
        game.powerups_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    #Level 2 waiting screen
    if waiting_for_level2:
        level2_box = pygame.Rect(140, 270, 520, 200)
        pygame.draw.rect(screen, GREY, level2_box)
        pygame.draw.rect(screen, YELLOW, level2_box, 3)
        complete_surface = font.render("LEVEL 01 COMPLETE", False, YELLOW)
        begin_surface = font.render("BEGIN LEVEL 02?", False, YELLOW)
        space_surface = font.render("PRESS SPACE", False, WHITE)
        screen.blit(complete_surface, complete_surface.get_rect(center=(400, 310)))
        screen.blit(begin_surface, begin_surface.get_rect(center=(400, 370)))
        screen.blit(space_surface, space_surface.get_rect(center=(400, 430)))

    pygame.display.update()
    clock.tick(60)