import pygame

from pygame.sprite import Sprite


class MouseBullet(Sprite):
    """A class to manage mouse's fired bullets"""

    def __init__(self, cm_game):
        super().__init__()
        self.screen = cm_game.screen
        self.settings = cm_game.settings
        self.m_color = self.settings.m_bullet_color

        # Create the mouse's bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.m_bullet_width, self.settings.m_bullet_height)
        self.rect.midleft = cm_game.mouse.rect.midleft

        # Store the mouse's bullet position as a decimal value
        self.x = float(self.rect.x)

    def update(self):
        """Move the mouse's bullet up the screen."""
        # Update the decimal position of the bullet.
        self.x -= self.settings.m_bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the mouse's bullets to the screen."""
        pygame.draw.rect(self.screen, self.m_color, self.rect)