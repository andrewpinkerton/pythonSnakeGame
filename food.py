from random import randrange

import pygame as pg

from colors import Color
from game_manager import GameManager


class Food:
    """Food object to be consumed by the snake."""

    def __init__(self, x: int, y: int, size: int):
        self.x: int = x
        self.y: int = y
        self.size: int = size

    def draw_food(self, screen: pg.Surface) -> None:
        """Render food to the screen."""

        rect_values: tuple = (self.x, self.y, self.size, self.size)
        pg.draw.rect(screen, Color.FOOD, rect_values)
        
    def random_move(self, gm: GameManager) -> None:
        """Move food to random location."""

        self.x = randrange(0, int(gm.width - self.size), self.size)
        self.y = randrange(0, int(gm.height - self.size), self.size)

    def get_pos(self) -> tuple:
        """Get position of food."""

        return(self.x, self.y)