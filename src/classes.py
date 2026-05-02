"""
Classes Module
==============
Contains the core data models.

Classes:
    Settings: validates and stores maze configuration
    Maze: maze generation and pathfinding logic

"""
from __future__ import annotations
from sys import exit
import random

try:
    from pydantic import (
        BaseModel,
        Field,
        field_validator,
        model_validator)
except ImportError as error:
    print(error)
    exit(1)


class Settings(BaseModel):
    WIDTH: int = Field(ge=3, le=40)
    HEIGHT: int = Field(ge=3, le=40)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = None

    @field_validator('ENTRY', 'EXIT', mode="before")
    @classmethod
    def parse_tuple(cls, value: str) -> tuple[int, int]:
        clean = value.strip("() ")
        x, y = clean.split(",")
        return (int(x.strip()), int(y.strip()))

    @field_validator('OUTPUT_FILE', mode="after")
    @classmethod
    def validator_output_file(cls, name: str) -> str:
        _name = name.removesuffix('.txt')
        if not _name:
            raise ValueError("Output file name cannot be empty")
        if not _name[0].isalpha():
            raise ValueError(f"Output file must start with a letter: '{name}'")
        if not all(c.isalnum() or c in '_-' for c in _name):
            raise ValueError(f"Invalid output file name: '{name}'\n"
                             "Allowed: letters, numbers, _ and -")
        if not name.endswith('.txt'):
            raise ValueError(f'Incorrect output_file: {name}:\n'
                             'valid example: maze.txt')
        else:
            return name

    @model_validator(mode='after')
    def validator_maze(self) -> Settings:
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT
        if entry_x >= self.WIDTH or exit_x >= self.WIDTH:
            raise ValueError('Coordinates cannot exceed Width')
        if entry_y >= self.HEIGHT or exit_y >= self.HEIGHT:
            raise ValueError('Coordinates cannot exceed Height')
        if any(c < 0 for c in (*self.ENTRY, *self.EXIT)):
            raise ValueError('Coordinates cannot be negative')
        if self.ENTRY == self.EXIT:
            raise ValueError('Entry and Exit cannot be the same cell')
        return self

    def __str__(self) -> str:
        return ("\n=== Settings === \n"
                f"\nWidth: {self.WIDTH}\n"
                f"Height: {self.HEIGHT}\n"
                f"Entry: {self.ENTRY}\nExit: {self.EXIT}\n"
                f"\nOutput_file: {self.OUTPUT_FILE}\n"
                f"Perfect: {self.PERFECT}\n"
                f"Seed: {self.SEED}\n")


class Maze:
    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings
        self.WIDTH: int = settings.WIDTH
        self.HEIGHT: int = settings.HEIGHT
        self.ENTRY: tuple[int, int] = settings.ENTRY
        self.EXIT: tuple[int, int] = settings.EXIT
        self.OUTPUT_FILE: str = settings.OUTPUT_FILE
        self.PERFECT: bool = settings.PERFECT
        self.SEED: int | None = settings.SEED
        self.grid: list[list[int]] | None = None

    def __str__(self) -> str:
        if self.grid is None:
            return "Maze not generated yet"
        grid: list[list[int]] = self.grid
        return '\n'.join(
            ''.join(format(cell, 'X') for cell in row)
            for row in grid
        )

    def save_maze(self) -> None:
        if self.grid is None:
            raise ValueError("Maze not generated yet")
        with open(self.settings.OUTPUT_FILE, 'w') as f:
            for row in self.grid:
                f.write(''.join(format(cell, 'X') for cell in row) + '\n')

    def generate(self) -> None:
        NORTH = 0x1
        EAST = 0x2
        SOUTH = 0x4
        WEST = 0x8

        DIRECTIONS = {
            NORTH: (0, -1),
            EAST:  (1,  0),
            SOUTH: (0,  1),
            WEST:  (-1, 0)}

        OPPOSITE = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST:  WEST,
            WEST:  EAST}

        rng = random.Random(self.SEED)

        # 1. Start: Fill grid with 0xF
        self.grid = [
            [0xF] * self.WIDTH for _ in range(self.HEIGHT)]

        # 2. DFS
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = [self.ENTRY]
        visited.add(self.ENTRY)

        while stack:
            x, y = stack[-1]
            dirs = list(DIRECTIONS.keys())
            rng.shuffle(dirs)
            carved = False
            for direction in dirs:
                dx, dy = DIRECTIONS[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.WIDTH and 0 <= ny < self.HEIGHT:
                    if (nx, ny) not in visited:
                        self.grid[y][x] &= ~direction
                        self.grid[ny][nx] &= ~OPPOSITE[direction]
                        visited.add((nx, ny))
                        stack.append((nx, ny))
                        carved = True
                        break
            if not carved:
                stack.pop()

        # 3. If perfect=false, remove extra walls
        if not self.PERFECT:
            for _ in range(self.WIDTH * self.HEIGHT // 4):
                x = rng.randint(0, self.WIDTH - 2)
                y = rng.randint(0, self.HEIGHT - 2)
                direction = rng.choice([EAST, SOUTH])
                dx, dy = DIRECTIONS[direction]
                self.grid[y][x] &= ~direction
                self.grid[y+dy][x+dx] &= ~OPPOSITE[direction]
