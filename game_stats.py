class GameStats():
    """Statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialise statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Game start in nonactive status
        self.game_active = False

        # The record must be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialise statistics, changing during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
