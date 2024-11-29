import pygame as pg


class GameManager:
    """Manages the game state."""

    def __init__(self, clock: pg.time.Clock):
        self.width: int = 800
        self.height: int = 800
        self.game_speed: int = 10
        self.segment_size: int = self.width // 20

        self.game_running: bool = True
        self.in_main_menu: bool = True
        self.in_game: bool = False
        self.game_over: bool = False

        self.clock : pg.time.Clock = clock
        self.fonts: dict = {
            "large": pg.font.Font(None, 72),
            "small": pg.font.Font(None, 36),
        }

    def tick(self) -> None:
        """Controls the frame rate of the game"""

        self.clock.tick(self.game_speed)

    def center(self) -> tuple:
        """Returns the center of the screen."""

        return (self.width // 2, self.height // 2)
