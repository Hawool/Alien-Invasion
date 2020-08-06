import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class of control ship's bullets"""

    def __init__(self, ai_settings, screen, ship):
        """Creating object of bullet in ship's position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Creating bullet in 0:0 position and assigning right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Bullet's position keep in float format
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move bullet to screen top"""
        # Update position in float format
        self.y -= self.speed_factor
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Output bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
