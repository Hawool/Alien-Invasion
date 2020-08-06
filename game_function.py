import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, stats,
                         play_button, ship,
                         aliens, bullets):
    """Response to press keys"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Creating new bullet and adding it in bullet's group
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Response to up keys"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb,
                 play_button, ship,
                 aliens, bullets):
    """Check mouse and button events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb,
                              play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats,
                                 play_button, ship,
                                 aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Starts a new game when the Play button is pressed"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Clear game settings
        ai_settings.initialize_dynamic_settings()

        # Hide cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset value and level images
        sb.prep_level()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_ships()

        # Clear alien and bullet lists
        aliens.empty()
        bullets.empty()

        # Create new fleet and position ship in center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Creating bullet if max not achieved"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creating alien's fleet"""
    # Creating alien and calculate number aliens in row
    # Interval between alien equal width alien

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Creating first alien's row
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create and place alien
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculate alien's number in row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create and place alien"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calculate number of alien row"""
    available_space_y = (ai_settings.screen_height -
                         (2 * alien_height) - 4 * ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """Reacts when an alien reaches the edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Change alien's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Hit alien with ship"""
    if stats.ships_left > 0:
        # Decrease ships_left.
        stats.ships_left -= 1

        # Update game info
        sb.prep_ships()

        # Clear alien and bullets lists
        aliens.empty()
        bullets.empty()

        # Create new fleet and position it in center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(ai_settings, stats, sb, screen, ship, bullets, aliens,
                  play_button):
    """Update screen and show new screen"""
    screen.fill(ai_settings.bg_color)
    # All bullets creating behind ship's image and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)
    # Output score
    sb.show_score()
    # Play button is showed if game is nonactive
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb,
                   ship, aliens, bullets):
    """Update bullet position and delete old bullets"""
    # Update bullet position
    bullets.update()

    # Delete old bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """Checking bullet hit to alien"""
    # If hit was then delete bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)
    if len(aliens) == 0:
        # Delete being bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        # Increase level
        stats.level += 1
        sb.prep_level()


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Checks if the aliens have made it to the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Happens is the same as in a collision with a ship.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, aliens, ship, bullets):
    """
    Checks if the fleet has reached the edge of the screen,
    after which it updates the positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Check collision "Alien-ship"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # Checking aliens who have reached the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens,
                        bullets)


def check_high_score(stats, sb):
    """Checks if a new record has appeared."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
