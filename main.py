from enum import Enum

import pygame
from pygame import Surface
from pygame.rect import Rect

CAPTION = "Snek - Every Masterpiece Got Its Cheap Copy"
FIELD_SIZE = (30, 30)
SCREEN_SIZE = (600, 600)
FPS = 1

ASSETS = {
    0: pygame.image.load("assets/grass.png"), 
    3: pygame.image.load("assets/ns_part.png"),
}


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 4
    Right = 7


class Block:
    def __init__(self, id: int, pos: tuple[int, int]) -> None:
        self.__id = id
        self.__x, self.__y = pos

    @property
    def id(self) -> int:
        return self.__id

    @property
    def position(self) -> tuple[int, int]:
        return (self.__x, self.__y)

    @position.setter
    def position(self, new: tuple[int, int]) -> None:
        self.__x, self.__y = new

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, new: int) -> None:
        self.__x = new

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, new: int) -> None:
        self.__y = new

    def draw(self, surface: Surface) -> None:
        asset = ASSETS[self.id]
        surface.blit(asset, self.position)


class Part(Block):
    def __init__(
        self,
        pos: tuple[int, int],
        front_dir: Direction,
        back_dir: Direction,
        id: int = 3,  # precomputed value for part of up & down direction
    ) -> None:
        super().__init__(id, pos)
        self.__fdir = front_dir
        self.__bdir = back_dir

    @property
    def direction(self) -> tuple[Direction, Direction]:
        return (self.__fdir, self.__bdir)

    @direction.setter
    def direction(self, new: tuple[Direction, Direction]) -> None:
        self.__fdir = new[0]
        self.__bdir = new[1]

    def update_id(self) -> None:
        self.__id = self.__fdir.value + self.__bdir.value


class Snake:
    def __init__(
        self,
        init_pos: tuple[int, int],
        init_dir: tuple[Direction, Direction],
    ) -> None:
        self.__parts = [
            # Head of Snake
            Part(init_pos, init_dir[0], init_dir[1]),
            # Tail
            Part(
                (init_pos[0], init_pos[1] + FIELD_SIZE[1]),
                *init_dir,
            ),
        ]

    def draw(self, surface: Surface) -> None:
        for part in self.__parts:
            part.draw(surface)

    def update(self) -> None:
        """Move the snake forward by passing the directions of the previous
        block to the next one and updating the position."""
        head = self.__parts[0]
        new = head
        old = None
        # update tail
        for part in self.__parts[1:]:
            old = part
            part.direction = new.direction
            part.position = new.position
            new = old

        # new head position
        match head.direction[0]:
            case Direction.Up:
                head.y -= FIELD_SIZE[1]
            case Direction.Down:
                head.y += FIELD_SIZE[1]
            case Direction.Left:
                head.x -= FIELD_SIZE[0]
            case Direction.Right:
                head.x += FIELD_SIZE[0]


class Map:
    def __init__(self) -> None:
        self.__map: list[list[Block]]

    def load_map(self, path: str):
        with open(path, "r") as f:
            temp = []
            x = 0
            for line in f.readlines():
                temp.append([])
                y = 0
                for i in line.split(","):
                    temp[-1].append(Block(int(i), (x, y)))
                    y += FIELD_SIZE[1]
                x += FIELD_SIZE[0]
            self.__map = temp

    def draw(self, surface: Surface) -> None:
        for row in self.__map:
            for block in row:
                asset = ASSETS[block.id]
                surface.blit(asset, block.position)


if __name__ == "__main__":
    # initiate pygame
    pygame.init()
    clock = pygame.time.Clock()

    # initialize game components
    world_map = Map()
    world_map.load_map("maps/level0.txt")
    snake = Snake((30, 300), (Direction.Up, Direction.Down))

    # setup screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)

    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # draw stuff
        world_map.draw(screen)
        snake.draw(screen)

        # update
        snake.update()
        print("loop")

        # update content on screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
