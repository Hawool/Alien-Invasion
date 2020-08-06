class Settings():
    """Class for keeking settings of Alien Invasion"""

    def __init__(self):
        """Initialise static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (196, 196, 196)
        self.ship_limit = 3

        # Settings of bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3

        # Settings of aliens
        self.fleet_drop_speed = 5
        # fleet_direction = 1 mean move to right, -1 to left

        # Game rate speed
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # Сost growth rate
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialise dynamic settings, changing during the game."""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        # fleet_direction = 1 mean move to right; and -1 - to left.
        self.fleet_direction = 1

        # Calculate score
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
