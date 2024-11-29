import sys

import pygame as pg

from game_manager import GameManager
from colors import Color
from snake import Snake
from direction import Direction
from food import Food


def main():
    pg.init()

    gm: GameManager = GameManager(pg.time.Clock())
    screen: pg.Surface = pg.display.set_mode((gm.width, gm.height))
    pg.display.set_caption("Snake")

    pg.mixer.music.load("audio/music.ogg")
    pg.mixer.music.set_volume(0.1)
    pg.mixer.music.play(-1)

    while gm.game_running:
        menu_loop(screen, gm)
        game_loop(screen, gm)
        game_over_loop(screen, gm)

    pg.quit()
    sys.exit()


def game_loop(screen: pg.Surface, gm: GameManager):
    """The game loop."""

    snake: Snake = Snake(gm.center(), gm.segment_size)

    food: Food = Food(0, 0, gm.segment_size)
    food.random_move(gm)
    while snake.colliding_with_body(food.get_pos()):
        food.random_move(gm)

    while gm.in_game:
        gm.tick()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gm.game_running = False
                gm.in_game = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and snake.head.direction != Direction.DOWN:
                    snake.head.direction = Direction.UP
                if event.key == pg.K_DOWN and snake.head.direction != Direction.UP:
                    snake.head.direction = Direction.DOWN
                if event.key == pg.K_RIGHT and snake.head.direction != Direction.LEFT:
                    snake.head.direction = Direction.RIGHT
                if event.key == pg.K_LEFT and snake.head.direction != Direction.RIGHT:
                    snake.head.direction = Direction.LEFT

        screen.fill(Color.BACKGROUND)
        snake.move()

        hit_wall: bool = snake.colliding_with_walls(screen)
        hit_body: bool = snake.colliding_with_body(snake.head.get_pos(), 1)
        if hit_wall or hit_body:
            gm.in_game = False
            gm.game_over = True
        elif snake.colliding_with_food(food):
            pg.mixer.Sound(snake.gulp).play()
            snake.add_segment()
            food.random_move(gm)
            while snake.colliding_with_body(food.get_pos()):
                food.random_move(gm)
        
        food.draw_food(screen)
        snake.draw_snake(screen)
        pg.display.flip()


def menu_loop(screen: pg.Surface, gm: GameManager) -> None:
    """The main menu loop."""

    while gm.in_main_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gm.game_running = False
                gm.in_main_menu = False
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                gm.in_main_menu = False
                gm.in_game = True
                break

        screen.fill(Color.BACKGROUND)

        display_menu_text(
            screen,
            gm,
            [">-<8==SNAKE=====>", "Press ENTER to start.", "by Andrew Pinkerton"]
        )

        pg.display.flip()
        gm.tick()


def game_over_loop(screen: pg.Surface, gm: GameManager) -> None:
    """The game over loop."""

    while gm.game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gm.game_running = False
                gm.game_over = False
                break
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                gm.in_main_menu = True
                gm.game_over = False
                break

        screen.fill(Color.BACKGROUND)

        display_menu_text(
            screen,
            gm,
            ["GAME OVER!", "Press ENTER to play again.", "by Andrew Pinkerton"]
        )

        pg.display.flip()
        gm.tick()


def display_menu_text(
    screen: pg.Surface,
    gm: GameManager,
    text: list,
) -> None:
    """Display the main text and instructions to the screen."""

    center: tuple = gm.center()
    offset: int = 0

    for i, item in enumerate(text):
        if i == 0:
            font: pg.font.Font = gm.fonts["large"]
        else:
            font: pg.font.Font = gm.fonts["small"]

        surface: pg.surface = font.render(item, True, Color.TEXT)
        rect: pg.Rect = surface.get_rect(center=center).move(0, offset)
        screen.blit(surface, rect)
        offset += surface.get_height() + 10


if __name__ == "__main__":
    main()