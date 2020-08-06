import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialise the ship and sets its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        # Load ship image and get rect
        self.image = pygame.image.load('images/ship_bmp.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        # Every new ship is created around bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # moving flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ship's position in view of flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.centerx += 1
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx -= 1
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """Draw ship in current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Position ship in bottom center"""
        self.center = self.screen_rect.centerx
