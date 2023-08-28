import pygame

import os


class Settings:
    """A class to store settings for The Arch Enemies"""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (36, 86, 43)
        self.border = pygame.Rect(self.screen_width//2, 0, 10, self.screen_height)
        self.black = (0, 0, 0)

        # Bullet settings for the cat
        self.c_bullet_speed = 2.0
        self.c_bullet_width = 13
        self.c_bullet_height = 6
        self.c_bullet_color = (61, 116, 117)
        self.c_bullet_allowed = 10

        # Bullet settings for the mouse
        self.m_bullet_speed = 3.0
        self.m_bullet_width = 10
        self.m_bullet_height = 3
        self.m_bullet_color = (136, 175, 149)
        self.m_bullet_allowed = 5

        # Health
        self.cat_health = 10
        self.mouse_health = 10

        # Text color
        self.black = (0, 0, 0)

        # Sound
        self.bullet_sound = pygame.mixer.Sound(os.path.join("Components", "shotgun.mp3"))
        self.hit_sound = pygame.mixer.Sound(os.path.join("Components", "hit.mp3"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join("Components", "game_over.mp3"))
