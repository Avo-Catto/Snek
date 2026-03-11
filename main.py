from collections.abc import Callable
from copy import copy
from enum import Enum
from random import randint

import pygame
from pygame import Surface

CAPTION = "Snek - Every Masterpiece Got Its Cheap Copy"
FIELD_SIZE = (30, 30)
BOARD_SIZE = (20, 20)
SCREEN_SIZE = (FIELD_SIZE[0] * BOARD_SIZE[0], FIELD_SIZE[1] * BOARD_SIZE[1])
FPS = 60

START_BUTTON = "assets/play_button.png"
GAME_OVER = "assets/game_over.png"
MAPS = (
    "maps/Level 1.txt",
    "maps/Level 2.txt",
    "maps/Level 3.txt",
)
LEVEL_UP_SEC = 3

ASSETS = {
    0: pygame.image.load("assets/grass.png"),
    1: pygame.image.load("assets/log.png"),
    2: pygame.image.load("assets/apple.png"),
    3: pygame.image.load("assets/cherry.png"),
    4: pygame.image.load("assets/head.png"),
    5: pygame.image.load("assets/part.png"),
    6: pygame.image.load("assets/curve.png"),
    7: pygame.image.load("assets/tail.png"),
}

# Initialialyze music & sounds
pygame.mixer.init()
pygame.mixer.music.load("sounds/8bit.mp3")

SOUNDS = {
    "eat": pygame.mixer.Sound("sounds/eat.mp3"),
    "eat2": pygame.mixer.Sound("sounds/eat2.mp3"),
    "game_over": pygame.mixer.Sound("sounds/game_over.mp3"),
    "level_up": pygame.mixer.Sound("sounds/level_up.mp3"),
}


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 4
    Right = 7


def direction_from_str(dir: str) -> Direction:
    """u = up; d = down; l = left; r = right"""
    match dir:
        case "u":
            return Direction.Up
        case "d":
            return Direction.Down
        case "l":
            return Direction.Left
        case "r":
            return Direction.Right
        case _:
            print(f"Error: Parsing Direction: {dir}")
            exit(1)


def counter_direction(dir: Direction) -> Direction:
    match dir:
        case Direction.Up:
            return Direction.Down
        case Direction.Down:
            return Direction.Up
        case Direction.Left:
            return Direction.Right
        case Direction.Right:
            return Direction.Left


class Block:
    def __init__(self, id: int, coord: tuple[int, int]) -> None:
        self.__id = id
        self.__coord = coord

    @property
    def id(self) -> int:
        return self.__id

    @property
    def position(self) -> tuple[int, int]:
        x, y = self.__coord
        return (x * FIELD_SIZE[0], y * FIELD_SIZE[1])

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__coord

    @coordinates.setter
    def coordinates(self, new: tuple[int, int]) -> None:
        self.__coord = new

    @property
    def x(self) -> int:
        return self.__coord[0]

    @x.setter
    def x(self, new: int) -> None:
        self.__coord = (new, self.y)

    @property
    def y(self) -> int:
        return self.__coord[1]

    @y.setter
    def y(self, new: int) -> None:
        self.__coord = (self.x, new)

    def draw(self, surface: Surface) -> None:
        asset = ASSETS[self.id]
        surface.blit(asset, self.position)


class Apple(Block):
    def __init__(
        self,
        coords: tuple[int, int] = (-1, -1),
        id: int = 2,
    ) -> None:
        super().__init__(id, coords)
        self.previous_coords = coords

    def eat(self) -> None:
        """Hide apple."""
        self.previous_coords = self.coordinates
        self.coordinates = (-1, -1)
        pygame.mixer.Sound.play(SOUNDS["eat"])

    def spawn(self, obstacles: list[Callable[[tuple[int, int]], bool]]) -> None:
        """Spawn an apple at a random empty space on the map."""
        coords = (randint(0, BOARD_SIZE[0]), randint(0, BOARD_SIZE[1]))
        if any([f(coords) for f in obstacles]) and coords != self.previous_coords:
            self.spawn(obstacles)
        else:
            self.coordinates = coords

    def is_collision(self, coordinates: tuple[int, int]) -> bool:
        if self.coordinates == coordinates:
            return True
        else:
            return False


class Cherry(Apple):
    def __init__(self, time: int, pos=(-1, -1), id=3) -> None:
        super().__init__(pos, id)
        self.life_time = 0
        self.out_time = 0
        self.cherry_time = time

    def eat(self) -> None:
        self.coordinates = (-1, -1)
        print("cherry eaten!\n\n")
        pygame.mixer.Sound.play(SOUNDS["eat2"])
        self.life_time = 0

    def spawn(self, obstacles):
        self.life_time = FPS * self.cherry_time
        return super().spawn(obstacles)

    def update(
        self,
        out_range: tuple[int, int],
        obstacles: list[Callable[[tuple[int, int]], bool]],
    ) -> None:
        if self.life_time == 0:
            self.coordinates = (-1, -1)
            self.out_time = FPS * randint(*out_range)
        elif self.out_time >= 0:
            self.out_time -= 1
        elif self.life_time < 0:
            self.spawn(obstacles)
        self.life_time -= 1


class DirectionBlock(Block):
    def __init__(
        self,
        id: int,
        pos: tuple[int, int],
        dir: tuple[Direction, Direction],
    ) -> None:
        super().__init__(id, pos)
        self.__dir = dir

    @property
    def direction(self) -> tuple[Direction, Direction]:
        return self.__dir

    @direction.setter
    def direction(self, new: tuple[Direction, Direction]) -> None:
        self.__dir = new

    def draw(self, surface: Surface) -> None:
        asset = ASSETS[self.id]
        fdir, _ = self.direction
        match fdir.value:
            case 1:
                rotation = 0
            case 2:
                rotation = 180
            case 4:
                rotation = 90
            case 7:
                rotation = -90
        rotated = pygame.transform.rotate(asset, rotation)
        surface.blit(rotated, self.position)


class Head(DirectionBlock):
    def __init__(
        self,
        pos: tuple[int, int],
        dir: tuple[Direction, Direction],
        id: int = 4,
    ) -> None:
        super().__init__(id, pos, dir)


class Tail(DirectionBlock):
    def __init__(
        self,
        pos: tuple[int, int],
        dir: tuple[Direction, Direction],
        id: int = 7,
    ) -> None:
        super().__init__(id, pos, dir)


class Part(DirectionBlock):
    def __init__(
        self,
        pos: tuple[int, int],
        dir: tuple[Direction, Direction],
        id: int = 5,
    ) -> None:
        super().__init__(id, pos, dir)

    def draw(self, surface: Surface) -> None:
        rotation = 0
        fdir, bdir = self.direction
        if fdir == counter_direction(bdir):
            asset = ASSETS[self.id]
            match fdir.value:
                case 1:
                    rotation = 0
                case 2:
                    rotation = 180
                case 4:
                    rotation = 90
                case 7:
                    rotation = -90
        else:
            asset = ASSETS[6]
            match fdir.value + bdir.value:
                case 5:
                    rotation = 180
                case 8:
                    rotation = 90
                case 6:
                    rotation = -90
                case 9:
                    rotation = 0

        rotated = pygame.transform.rotate(asset, rotation)
        surface.blit(rotated, self.position)


class Snake:
    def __init__(
        self,
        init_pos: tuple[int, int],
        init_dir: tuple[Direction, Direction],
    ) -> None:
        self.__move = True
        self.__parts = [
            Head(init_pos, init_dir),
            Tail((init_pos[0], init_pos[1] + 1), init_dir),
        ]
        self.score = 0

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__parts[0].coordinates

    @property
    def position(self) -> tuple[int, int]:
        return self.__parts[0].position

    def draw(self, surface: Surface) -> None:
        for part in self.__parts:
            part.draw(surface)

    def set_direction(self, dir: Direction) -> None:
        _, bdir = self.__parts[0].direction
        if dir != bdir:
            self.__parts[0].direction = (dir, bdir)

    def grow(self) -> None:
        self.__move = True
        head = self.__parts[0]
        self.__parts.insert(1, Part(head.coordinates, head.direction))
        self.score += 1

    def update(self, move: bool) -> None:
        """Move the snake forward by passing the directions of the previous
        block to the next one and updating the position."""
        head = self.__parts[0]
        new = head
        old = None

        # update tail
        if move:
            for part in self.__parts[1:]:
                old = copy(part)
                part.direction = new.direction
                part.coordinates = new.coordinates
                new = old  # old becomes head for some reason

        # new head position
        match head.direction[0]:
            case Direction.Up:
                head.y -= 1
            case Direction.Down:
                head.y += 1
            case Direction.Left:
                head.x -= 1
            case Direction.Right:
                head.x += 1

        # make head straight
        fdir, _ = head.direction
        head.direction = (fdir, counter_direction(fdir))

    def is_collision(self, coordinates: tuple[int, int]) -> bool:
        """Check if snake collides with itself."""
        for part in self.__parts[1:]:
            if coordinates == part.coordinates:
                return True
        else:
            return False


class UnknownParameter(Exception):
    def __str__(self) -> str:
        return ""


class Map:
    def __init__(self) -> None:
        self.__map: list[list[Block]] = []
        self.speed = 0
        self.cherries = False
        self.next_after = 10
        self.snake_coord = (10, 10)
        self.snake_dir = Direction.Up
        self.cherry_time = 4
        self.cherry_out_time = (5, 10)

    def load_map(self, path: str):
        try:
            with open(path, "r") as f:
                temp = []
                x = 0
                for line in f.readlines():
                    if line.startswith(">"):
                        content = line.split()
                        match content[1].lower():
                            case "speed":
                                self.speed = int(content[2])
                            case "cherries":
                                self.cherries = bool(content[2])
                            case "next":
                                self.next_after = int(content[2])
                            case "snake_pos":
                                self.snake_coord = (int(content[2]), int(content[3]))
                            case "snake_dir":
                                self.snake_dir = direction_from_str(content[2])
                            case "cherry_time":
                                self.cherry_time = int(content[2])
                            case "cherry_out_time":
                                self.cherry_out_time = (
                                    int(content[2]),
                                    int(content[3]),
                                )
                            case _:
                                print(
                                    f"Error: Unknown Parameter in Level File: {content}"
                                )
                                exit(1)
                    else:
                        temp.append([])
                        y = 0
                        for i in line.split(","):
                            temp[-1].append(Block(int(i), (x, y)))
                            y += 1
                        x += 1
                self.__map = temp
        except Exception as e:
            print(f"Failed loading map: {path}\nError: {e}")
            exit(1)

    def draw(self, surface: Surface) -> None:
        for row in self.__map:
            for block in row:
                asset = ASSETS[block.id]
                surface.blit(asset, block.position)

    def is_collision(self, pos: tuple[int, int]) -> bool:
        """Check if there is an obstacle or border at the given position."""
        # check borders
        x, y = pos
        if any(
            [
                x + 1 > BOARD_SIZE[0],
                y + 1 > BOARD_SIZE[1],
                x < 0,
                y < 0,
            ]
        ):
            return True
        # check obstacle
        if self.__map[x][y].id != 0:
            return True
        else:
            return False


def start_screen(surface: Surface, clock: pygame.time.Clock) -> bool:
    """Show an interrupting button that returns False if exited and True if pressed."""

    # load button asset
    asset = pygame.image.load(START_BUTTON)
    button = pygame.transform.scale(asset, SCREEN_SIZE)

    # button hitbox
    width = SCREEN_SIZE[0] / 3
    height = SCREEN_SIZE[1] / 3
    x = (SCREEN_SIZE[0] / 2) - (width / 2)
    y = (SCREEN_SIZE[1] / 2) - (height / 2) + 50
    button_hitbox = pygame.Rect(x, y, width, height)

    while True:
        # handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        surface.blit(button, (0, 0))
        mousepos = pygame.mouse.get_pos()
        if button_hitbox.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0]:
                return True

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(surface: Surface, clock: pygame.time.Clock) -> bool:
    """Game over screen that returns False if exited and True if pressed."""

    # load assets
    asset = pygame.image.load(GAME_OVER)
    image = pygame.transform.scale(asset, SCREEN_SIZE)

    while True:
        # handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        surface.blit(image, (0, 0))
        if pygame.mouse.get_pressed()[0]:
            return True

        pygame.display.flip()
        clock.tick(FPS)


def level_up_screen(surface: Surface, clock: pygame.time.Clock, level: int) -> bool:
    try:  # extract name of level
        name = MAPS[level].split("/")[-1].split(".")[0]
    except Exception:
        print(f'Error: Extracting level name failed: "{MAPS[level]}"')
        exit(1)

    # render text
    font = pygame.font.Font(None, 64)
    text = font.render(name, True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = (int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 2))

    # for LEVEL_UP_SEC show this screen & then just continue
    i = 0
    while i < FPS * LEVEL_UP_SEC:
        i += 1

        # handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        surface.blit(text, rect)
        if pygame.mouse.get_pressed()[0]:
            return True

        pygame.display.flip()
        clock.tick(FPS)
    return True


def you_won_screen(surface: Surface, clock: pygame.time.Clock):
    font = pygame.font.Font(None, 64)
    text = font.render("You won I guess -_-", True, (255, 255, 255))
    rect = text.get_rect()
    rect.center = (int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 2))

    while True:
        # handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        surface.blit(text, rect)
        if pygame.mouse.get_pressed()[0]:
            exit()

        pygame.display.flip()
        clock.tick(FPS)


def main():
    # initiate pygame
    pygame.init()
    clock = pygame.time.Clock()

    # setup screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)

    # interrupt with start screen
    if not start_screen(screen, clock):
        exit()

    # setup game
    level = 0
    level_up = False
    score_font = pygame.font.Font(None, 22)

    # retry after game over
    retry = True
    while retry:
        # check if won
        if level == len(MAPS):
            you_won_screen(screen, clock)

        # initialize game components
        world_map = Map()
        world_map.load_map(MAPS[level])
        snake = Snake(
            world_map.snake_coord,
            (world_map.snake_dir, counter_direction(world_map.snake_dir)),
        )
        apple = Apple()
        apple.spawn([snake.is_collision, world_map.is_collision])
        cherry = Cherry(world_map.cherry_time)
        print(world_map.cherries)
        if world_map.cherries:
            cherry.spawn(
                [snake.is_collision, world_map.is_collision, apple.is_collision]
            )

        if level_up:
            if not level_up_screen(screen, clock, level):
                exit()

        # post-setup
        counter = 0
        level_up = False
        pygame.mixer.music.play(-1)

        # game loop
        running = True
        while running:
            counter += 1

            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                # controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.set_direction(Direction.Up)
                    if event.key == pygame.K_DOWN:
                        snake.set_direction(Direction.Down)
                    if event.key == pygame.K_LEFT:
                        snake.set_direction(Direction.Left)
                    if event.key == pygame.K_RIGHT:
                        snake.set_direction(Direction.Right)

            if counter >= FPS - world_map.speed:
                counter = 0

                # eat apple
                move = True
                if snake.position == apple.position:
                    apple.eat()
                    apple.spawn(
                        [
                            snake.is_collision,
                            world_map.is_collision,
                            cherry.is_collision,
                        ]
                    )
                    snake.grow()
                    move = False

                # eat cherry
                if snake.position == cherry.position:
                    cherry.eat()
                    snake.grow()
                    snake.score += 1
                    move = False

                # check if level up
                if snake.score >= world_map.next_after:
                    pygame.mixer.Sound.play(SOUNDS["level_up"])
                    running = False
                    level_up = True
                    level += 1

                # update
                snake.update(move)

                # collision
                x, y = snake.position
                if any(
                    [
                        snake.is_collision(snake.coordinates),
                        world_map.is_collision(snake.coordinates),
                    ]
                ):
                    pygame.mixer.Sound.play(SOUNDS["game_over"])
                    running = False

                # draw stuff
                world_map.draw(screen)
                apple.draw(screen)
                cherry.draw(screen)
                snake.draw(screen)
                text = score_font.render(
                    f"Score: {snake.score} / {world_map.next_after}",
                    True,
                    (255, 255, 255),
                )
                screen.blit(text, (2, 2))

                # update content on screen
                pygame.display.flip()

            # update cherry
            if world_map.cherries:
                cherry.update(
                    world_map.cherry_out_time,
                    [snake.is_collision, world_map.is_collision, apple.is_collision],
                )

            # tick clock
            clock.tick(FPS)

        pygame.mixer.music.pause()
        if not level_up:
            retry = game_over_screen(screen, clock)
            level = 0

    pygame.quit()


if __name__ == "__main__":
    main()
