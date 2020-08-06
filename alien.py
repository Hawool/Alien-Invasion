import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class for one alien"""

    def __init__(self, ai_settings, screen):
        """Initiating alien and creating start position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load image
        self.image = pygame.image.load('images/alien_bmp_d.bmp')
        self.rect = self.image.get_rect()

        # Every new alien start in top left angle
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving position of alien
        self.x = float(self.rect.x)

    def blitme(self):
        """Output alien"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True, if alien around end of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move alien to right or left"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
