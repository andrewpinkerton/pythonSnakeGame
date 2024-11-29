import pygame as pg

from segment import Segment
from direction import Direction
from colors import Color
from food import Food


class Snake:
    """Class that manages the snake controlled by the player."""

    def __init__(self, pos: tuple, segment_size: int):
        self.segment_size: int = segment_size
        self.head: Segment = Segment(pos, Direction.UP)
        self.segments: list = [self.head]
        self.gulp: str = "audio/gulp.wav"

    def draw_snake(self, screen: pg.Surface) -> None:
        """Render the snake to the screen."""

        for segment in self.segments:
            rect_values: tuple = (segment.x, segment.y, self.segment_size, self.segment_size)
            pg.draw.rect(screen, Color.SNAKE, rect_values)

    def move(self) -> None:
        """Move each segment one size unit in its current direction and
        then update their current direction."""

        for segment in self.segments:
            segment.x += self.segment_size * segment.direction[0]
            segment.y += self.segment_size * segment.direction[1]

        self.update_directions()

    def update_directions(self) -> None:
        """Update the direction of each segment, beyond the first.
        Will start with last and work to the front"""

        for i in range(len(self.segments) - 1, 0, -1):
            before: Segment = self.segments[i - 1]
            new_dir: Direction = before.direction
            self.segments[i].direction = before.direction

    def add_segment(self) -> None:
        """Add a new segment to the end of the snake."""

        last: Segment = self.segments[-1]
        x: int  = last.x + self.segment_size * -last.direction[0]
        y: int  = last.y + self.segment_size * -last.direction[1]
        new: Segment = Segment((x, y), last.direction)

        self.segments.append(new)

    def colliding_with_food(self, food: Food) -> None:
        """Check if snake head is colliding with food."""

        return self.head.get_pos() == food.get_pos()

    def colliding_with_body(self, point: tuple, offset: int=0) -> bool:
        """Check if point is colliding with body."""

        for i, segment in enumerate(self.segments):
            if i >= offset and point == segment.get_pos():
                return True
        return False

    def colliding_with_walls(self, screen: pg.Surface) -> bool:
        """Check if the head is colling with edge of screen."""

        return(
            self.head.x < 0
            or self.head.x >= screen.get_width()
            or self.head.y < 0
            or self.head.y >= screen.get_height()
        )