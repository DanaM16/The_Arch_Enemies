import pygame
import sys
from settings import Settings
from cat import Cat
from mouse import Mouse
from cat_bullet import CatBullet
from mouse_bullet import MouseBullet

pygame.font.init()
pygame.mixer.init()


class CatMouse:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("The Arch Enemies")
        self.state = "INTRO"

        self.cat = Cat(self)
        self.cat_bullets = pygame.sprite.Group()
        self.mouse = Mouse(self)
        self.mouse_bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.cat.update()
            self.mouse.update()
            self.cat_bullets.update()
            self.mouse_bullets.update()
            self._check_bullet_collisions()
            self._update_cat_bullets()
            self._update_mouse_bullets()
            self._update_screen()

    def _check_events(self):
        # Respond to keypresses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif self.state == "INTRO" and event.type == pygame.KEYDOWN:
                self.state = "PLAY"
            elif self.state == "PLAY":
                if event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Quit botton
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_r:
            self._restart_game()
        # Cat's movement
        if event.key == pygame.K_d:
            self.cat.c_moving_right = True
        if event.key == pygame.K_a:
            self.cat.c_moving_left = True
        if event.key == pygame.K_w:
            self.cat.c_moving_up = True
        if event.key == pygame.K_s:
            self.cat.c_moving_down = True
        # Cat's bullet
        if event.key == pygame.K_SPACE:
            self.cat_fire_bullet()

        # Mouse's movement
        if event.key == pygame.K_RIGHT:
            self.mouse.m_moving_right = True
        if event.key == pygame.K_LEFT:
            self.mouse.m_moving_left = True
        if event.key == pygame.K_UP:
            self.mouse.m_moving_up = True
        if event.key == pygame.K_DOWN:
            self.mouse.m_moving_down = True
        # Mouse's bullet
        if event.key == pygame.K_RCTRL:
            self.mouse_fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        # Cat's movement
        if event.key == pygame.K_d:
            self.cat.c_moving_right = False
        if event.key == pygame.K_a:
            self.cat.c_moving_left = False
        if event.key == pygame.K_w:
            self.cat.c_moving_up = False
        if event.key == pygame.K_s:
            self.cat.c_moving_down = False
        # Mouse's movement
        if event.key == pygame.K_RIGHT:
            self.mouse.m_moving_right = False
        if event.key == pygame.K_LEFT:
            self.mouse.m_moving_left = False
        if event.key == pygame.K_UP:
            self.mouse.m_moving_up = False
        if event.key == pygame.K_DOWN:
            self.mouse.m_moving_down = False

    def cat_fire_bullet(self):
        """Create a new cat's bullet and add it to the bullets group."""
        if len(self.cat_bullets) < self.settings.c_bullet_allowed:
            cat_bullet = CatBullet(self)
            self.cat_bullets.add(cat_bullet)
            self.settings.bullet_sound.play()

    def mouse_fire_bullet(self):
        """Create a new mouse's bullet and add it to the bullets group."""
        if len(self.mouse_bullets) < self.settings.m_bullet_allowed:
            mouse_bullet = MouseBullet(self)
            self.mouse_bullets.add(mouse_bullet)
            self.settings.bullet_sound.play()

    def _update_cat_bullets(self):
        """Update cat's bullets position and get rid of old bullets."""
        # Get rid of cat's bullets that have disappeared.
        for new_c_bullet in self.cat_bullets.copy():
            if new_c_bullet.rect.left > self.settings.screen_width:
                self.cat_bullets.remove(new_c_bullet)
                # print(len(self.cat_bullets))

        # Check for collisions between cat's bullets and the mouse
        colliding_c_bullets = pygame.sprite.spritecollide(self.mouse, self.cat_bullets, True)
        # This also removes the bullet on the collision
        if colliding_c_bullets:
            self.settings.mouse_health -= 1
            self.settings.hit_sound.play()

        # Check for GAME_OVER condition
        if self.settings.mouse_health == 0:
            self.state = "CAT_WON"
            self.settings.game_over_sound.play()

    def _update_mouse_bullets(self):
        """Update mouse's bullets position and get rid of old bullets."""
        # Get rid of mouse's bullets that have disappeared.
        for new_m_bullet in self.mouse_bullets.copy():
            if new_m_bullet.rect.right < 0:
                self.mouse_bullets.remove(new_m_bullet)
                # print(len(self.mouse_bullets))

        # Check for collisions between mouse's bullets and the cat
        colliding_m_bullets = pygame.sprite.spritecollide(self.cat, self.mouse_bullets, True)
        # This also removes the bullet on the collision
        if colliding_m_bullets:
            self.settings.cat_health -= 1
            self.settings.hit_sound.play()

        # Check for GAME_OVER condition
        if self.settings.cat_health == 0:
            self.state = "MOUSE_WON"
            self.settings.game_over_sound.play()

    def _check_bullet_collisions(self):
        """Handle bullet-to-bullet collisions."""
        if pygame.sprite.groupcollide(self.cat_bullets, self.mouse_bullets, True, True):
            self.settings.hit_sound.play()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        #   Intro text
        if self.state == "INTRO":
            intro_font = pygame.font.SysFont("inkfree", 40)
            intro_text1 = intro_font.render("Welcome to 'The Arch Enemies'!", 1, (255, 255, 255))
            intro_text2 = intro_font.render("Cat: 'A' - left, 'W' - up, 'D' - right, 'S' - down, 'SPACE' - shoot", 1,
                                            (255, 255, 255))
            intro_text3 = intro_font.render("Mouse: left, up, right and down arrow, 'R_CTRL' - shoot", 1,
                                            (255, 255, 255))
            intro_text4 = intro_font.render("Press any key to start", 1, (255, 255, 255))

            # Determine the position of each line
            total_intro = intro_text1.get_height() + intro_text2.get_height() + intro_text3.get_height() + \
                intro_text4.get_height() + 20  # 20 is spacing between lines
            intro_y = self.settings.screen_height // 2 - total_intro // 2

            intro_text1_pos = (
                self.settings.screen_width // 2 - intro_text1.get_width() // 2,
                intro_y
            )
            intro_text2_pos = (
                self.settings.screen_width // 2 - intro_text2.get_width() // 2,
                intro_y + intro_text1.get_height() + 10  # Move it down by the height of text 1 and add some spacing
            )

            intro_text3_pos = (
                self.settings.screen_width // 2 - intro_text3.get_width() // 2,
                intro_y + intro_text1.get_height() + intro_text2.get_height() + 20
                #  Move it down by the height of text 1 and text 2 and add spacing
            )

            intro_text4_pos = (
                self.settings.screen_width // 2 - intro_text4.get_width() // 2,
                intro_y + intro_text1.get_height() + intro_text2.get_height() + intro_text3.get_height() + 30
                #  Move it down by the height of text 1, 2 and 3 and add spacing
            )

            self.screen.fill((0, 0, 0))  # Clear the screen
            self.screen.blit(intro_text1, intro_text1_pos)
            self.screen.blit(intro_text2, intro_text2_pos)
            self.screen.blit(intro_text3, intro_text3_pos)
            self.screen.blit(intro_text4, intro_text4_pos)

        # Health and win text
        self.health_font = pygame.font.SysFont("inkfree", 40)
        self.cat_hp = self.health_font.render("Health: " + str(self.settings.cat_health), 1, self.settings.black)
        self.mouse_hp = self.health_font.render("Health: " + str(self.settings.mouse_health), 1, self.settings.black)

        self.win_font = pygame.font.SysFont("inkfree", 40)
        self.cat_win = self.win_font.render("Cat Won!!", 1, (255, 0, 0), (0, 0, 0))

        if self.state == "PLAY":
            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.cat_hp, (10, 10))
            self.screen.blit(self.mouse_hp, (620, 10))
            pygame.draw.rect(self.screen, self.settings.black, self.settings.border)
            self.cat.blitme()
            self.mouse.blitme()

            for new_c_bullet in self.cat_bullets.sprites():
                new_c_bullet.draw_bullet()

            for new_m_bullet in self.mouse_bullets.sprites():
                new_m_bullet.draw_bullet()

        if self.state == "CAT_WON":
            # Render each line of text to a separate surface
            line1 = self.win_font.render("Purrfect Victory!!!", 1, (61, 116, 117), (0, 0, 0))
            line2 = self.win_font.render("Press 'R' for Restart", 1, (61, 116, 117), (0, 0, 0))
            line3 = self.win_font.render("Press 'ESC' for Quit", 1, (61, 116, 117), (0, 0, 0))

            # Determine the position of each line
            total_height = line1.get_height() + line2.get_height() + line3.get_height() + 20
            # 20 is spacing between lines
            starting_y = self.settings.screen_height // 2 - total_height // 2

            line1_pos = (
                self.settings.screen_width // 2 - line1.get_width() // 2,
                starting_y
            )
            line2_pos = (
                self.settings.screen_width // 2 - line2.get_width() // 2,
                starting_y + line1.get_height() + 10  # Move it down by the height of line 1 and add some spacing
            )

            line3_pos = (
                self.settings.screen_width // 2 - line3.get_width() // 2,
                starting_y + line1.get_height() + line2.get_height() + 20
                # Move it down by the height of line 1 and line 2 and add spacing
            )

            # Blit each line to the screen
            self.screen.blit(line1, line1_pos)
            self.screen.blit(line2, line2_pos)
            self.screen.blit(line3, line3_pos)

        elif self.state == "MOUSE_WON":
            # Render each line of text to a separate surface
            line1 = self.win_font.render("Mice work, champ!!!", 1, (136, 175, 149), (0, 0, 0))
            line2 = self.win_font.render("Press 'R' for Restart", 1, (136, 175, 149), (0, 0, 0))
            line3 = self.win_font.render("Press 'ESC' for Quit", 1, (136, 175, 149), (0, 0, 0))

            # Determine the position of each line
            total_height = line1.get_height() + line2.get_height() + line3.get_height() + 20
            # 20 is spacing between lines
            starting_y = self.settings.screen_height // 2 - total_height // 2

            line1_pos = (
                self.settings.screen_width // 2 - line1.get_width() // 2,
                starting_y
            )
            line2_pos = (
                self.settings.screen_width // 2 - line2.get_width() // 2,
                starting_y + line1.get_height() + 10  # Move it down by the height of line 1 and add some spacing
            )

            line3_pos = (
                self.settings.screen_width // 2 - line3.get_width() // 2,
                starting_y + line1.get_height() + line2.get_height() + 20
                # Move it down by the height of line 1 and line 2 and add spacing
            )

            # Blit each line to the screen
            self.screen.blit(line1, line1_pos)
            self.screen.blit(line2, line2_pos)
            self.screen.blit(line3, line3_pos)

        pygame.display.flip()

    def _restart_game(self):
        # Reset game attributes
        self.settings.cat_health = 10
        self.settings.mouse_health = 10

        # Reset any other game attributes
        self.state = "PLAY"


if __name__ == "__main__":
    # Make a game instance, and run the game.
    cm = CatMouse()
    cm.run_game()
