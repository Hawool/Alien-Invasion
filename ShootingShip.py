import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initialise game and create screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Create objects GameStats and Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Creating Ship
    ship = Ship(ai_settings, screen)
    # Creating bullets
    bullets = Group()
    aliens = Group()

    # Create play button
    play_button = Button(ai_settings, screen, "Play")

    # Create alien's fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:
        # Checking keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, sb,
                        play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            bullets.update()
            aliens.update()
            # Delete bullets behind screen
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets)
        # Update screen
        gf.update_screen(ai_settings, stats, sb, screen, ship, bullets, aliens,
                         play_button)


run_game()
