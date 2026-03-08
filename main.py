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


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 4
    Right = 7


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
    def __init__(self, id: int, pos: tuple[int, int]) -> None:
        self.__id = id
        self.__pos = pos

    @property
    def id(self) -> int:
        return self.__id

    @property
    def position(self) -> tuple[int, int]:
        x, y = self.__pos
        return (x * FIELD_SIZE[0], y * FIELD_SIZE[1])

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__pos

    @coordinates.setter
    def coordinates(self, new: tuple[int, int]) -> None:
        self.__pos = new

    @property
    def x(self) -> int:
        return self.__pos[0]

    @x.setter
    def x(self, new: int) -> None:
        self.__pos = (new, self.y)

    @property
    def y(self) -> int:
        return self.__pos[1]

    @y.setter
    def y(self, new: int) -> None:
        self.__pos = (self.x, new)

    def draw(self, surface: Surface) -> None:
        asset = ASSETS[self.id]
        surface.blit(asset, self.position)


class Apple(Block):
    def __init__(
        self,
        pos: tuple[int, int] = (-FIELD_SIZE[0], -FIELD_SIZE[1]),
        id: int = 2,
    ) -> None:
        super().__init__(id, pos)

    def eat(self) -> None:
        """Hide apple."""
        self.coordinates = (-FIELD_SIZE[0], -FIELD_SIZE[1])

    def spawn(self, obstacles: list[Callable[[tuple[int, int]], bool]]) -> None:
        """Spawn an apple at a random empty space on the map."""
        coords = (randint(0, BOARD_SIZE[0]), randint(0, BOARD_SIZE[1]))
        if any([f(coords) for f in obstacles]):
            self.spawn(obstacles)
        else:
            self.coordinates = coords


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
    pass


class Map:
    def __init__(self) -> None:
        self.__map: list[list[Block]] = []
        self.speed = 0
        self.cherries = False

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
                            case _:
                                raise UnknownParameter
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


if __name__ == "__main__":
    # initiate pygame
    pygame.init()
    clock = pygame.time.Clock()

    # initialize game components
    world_map = Map()
    world_map.load_map("maps/Level 2.txt")
    snake = Snake((1, 10), (Direction.Up, Direction.Down))
    apple = Apple()

    # setup screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)

    # set up game
    apple.spawn([snake.is_collision, world_map.is_collision])

    # game loop
    counter = 0
    running = True
    while running:
        counter += 1

        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # controls
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                if event.key == pygame.K_UP:
                    print("up")
                    snake.set_direction(Direction.Up)
                if event.key == pygame.K_DOWN:
                    print("down")
                    snake.set_direction(Direction.Down)
                if event.key == pygame.K_LEFT:
                    print("left")
                    snake.set_direction(Direction.Left)
                if event.key == pygame.K_RIGHT:
                    print("right")
                    snake.set_direction(Direction.Right)

        if counter >= FPS - world_map.speed:
            counter = 0

            # eat apple
            move = True
            if snake.position == apple.position:
                apple.eat()
                snake.grow()
                apple.spawn([snake.is_collision, world_map.is_collision])
                move = False

            # update
            snake.update(move)
            print("loop")

            # collision
            x, y = snake.position
            if any(
                [
                    snake.is_collision(snake.coordinates),
                    world_map.is_collision(snake.coordinates),
                ]
            ):
                print("Game Over!")
                running = False

            # draw stuff
            world_map.draw(screen)
            apple.draw(screen)
            snake.draw(screen)

            # update content on screen
            pygame.display.flip()

        # tick clock
        clock.tick(FPS)

    pygame.quit()
