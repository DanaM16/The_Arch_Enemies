import pygame

from pygame.sprite import Sprite


class CatBullet(Sprite):
    """A class to manage cat's fired bullets"""

    def __init__(self, cm_game):
        super().__init__()
        self.screen = cm_game.screen
        self.settings = cm_game.settings
        self.c_color = self.settings.c_bullet_color

        # Create the cat's bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.c_bullet_width, self.settings.c_bullet_height)
        self.rect.midright = cm_game.cat.rect.midright

        # Store the cat's bullet position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the cat's bullet up the screen."""
        # Update the decimal position of the bullet.
        self.x += self.settings.c_bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the cat's bullets to the screen."""
        pygame.draw.rect(self.screen, self.c_color, self.rect)
