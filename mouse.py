import pygame

from settings import Settings


class Mouse:
    """A class to manage the mouse."""

    def __init__(self, cm_game):
        """Initialize the mouse and set its starting position."""
        self.screen = cm_game.screen
        self.screen_rect = cm_game.screen.get_rect()
        self.settings = Settings()

        # Load the mouse image and get its rect.
        self.mouse = pygame.image.load("Components/mouse.png")
        self.rect = self.mouse.get_rect()

        # Start the mouse at the left side of the screen.
        self.rect.midright = self.screen_rect.midright

        # Movement flag
        self.m_moving_right = False
        self.m_moving_left = False
        self.m_moving_up = False
        self.m_moving_down = False

    def update(self):
        """Update the mouse's position based on the movement flag."""
        if self.m_moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 3
        if self.m_moving_left and self.rect.left > self.settings.screen_width//2 + 10:  # + 10 pixels
            self.rect.x -= 3
        if self.m_moving_up and self.rect.top > 0 - 3:  # - 3 pixels
            self.rect.y -= 3
        if self.m_moving_down and self.rect.bottom < self.screen_rect.bottom - 5:   # - 5 pixels
            self.rect.y += 3

    def blitme(self):
        """Draw the cat at its current location."""
        self.screen.blit(self.mouse, self.rect)
