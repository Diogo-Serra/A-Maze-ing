"""
Classes Module
==============
Contains the core data models.

Classes:
    Settings: validates and stores maze configuration
    MazeGenerator: maze generation and renderer and pathfinding logic
"""
from __future__ import annotations
from sys import exit

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

        PATTERN_W = 7
        PATTERN_H = 5
        if self.WIDTH >= PATTERN_W + 2 and self.HEIGHT >= PATTERN_H + 2:
            FOUR = [
                [1, 0, 1],
                [1, 0, 1],
                [1, 1, 1],
                [0, 0, 1],
                [0, 0, 1],
            ]
            TWO = [
                [1, 1, 1],
                [0, 0, 1],
                [1, 1, 1],
                [1, 0, 0],
                [1, 1, 1],
            ]
            start_x = (self.WIDTH - PATTERN_W) // 2
            start_y = (self.HEIGHT - PATTERN_H) // 2
            fixed: set[tuple[int, int]] = set()
            for row in range(PATTERN_H):
                for col in range(3):
                    if FOUR[row][col]:
                        fixed.add((start_x + col, start_y + row))
                    if TWO[row][col]:
                        fixed.add((start_x + 4 + col, start_y + row))
            for label, coord in (("Entry", self.ENTRY), ("Exit", self.EXIT)):
                if coord in fixed:
                    raise ValueError(
                        f"{label} {coord} overlaps with the '42' pattern")
        return self

    def show_settings(self) -> None:
        print("\n    ===== Settings ===== \n"
              f"\n    Width: {self.WIDTH}\n"
              f"    Height: {self.HEIGHT}\n"
              f"    Entry: {self.ENTRY}\n    Exit: {self.EXIT}\n"
              f"\n    Output_file: {self.OUTPUT_FILE}\n"
              f"    Perfect: {self.PERFECT}\n"
              f"    Seed: {self.SEED}\n"
              f"    {20 * '-'}")
