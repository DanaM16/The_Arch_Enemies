import pygame

from settings import Settings


class Cat:
    """A class to manage the cat."""

    def __init__(self, cm_game):
        """Initialize the cat and set its starting position."""
        self.screen = cm_game.screen
        self.screen_rect = cm_game.screen.get_rect()
        self.settings = Settings()

        # Load the cat image and get its rect.
        self.cat = pygame.image.load("Components/cat.png")
        self.rect = self.cat.get_rect()

        # Start the cat at the left side of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Movement flag
        self.c_moving_right = False
        self.c_moving_left = False
        self.c_moving_up = False
        self.c_moving_down = False

    def update(self):
        """Update the cat's position based on the movement flag."""
        if self.c_moving_right and self.rect.right < self.settings.screen_width//2:  # half of the width
            self.rect.x += 2
        if self.c_moving_left and self.rect.left > 0:
            self.rect.x -= 2
        if self.c_moving_up and self.rect.top > 0:
            self.rect.y -= 2
        if self.c_moving_down and self.rect.bottom < self.screen_rect.bottom - 7:   # - 7 pixels
            self.rect.y += 2

    def blitme(self):
        """Draw the cat at its current location."""
        self.screen.blit(self.cat, self.rect)
