from direction import Direction


class Segment:
    """A class to represent a segment of the snake."""

    def __init__(self, pos: tuple, direction: Direction):
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.direction: Direction = direction

    def get_pos(self) -> tuple:
        """Get the position of the segment."""

        return (self.x, self.y)