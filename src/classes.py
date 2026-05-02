"""
Classes Module
==============
Contains the core data models.

Classes:
    Settings: validates and stores maze configuration
    Maze: maze generation and pathfinding logic

"""


from sys import exit

try:
    from pydantic import ( # noqa
        BaseModel,
        Field,
        field_validator,
        model_validator,
        ValidationError)
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

    @field_validator('OUTPUT_FILE', mode="after")
    def validator_output_file(cls, name: str):
        file_name = name.strip()
        if not file_name.endswith('.txt'):
            raise ValueError(f'Incorrect output_file: {name}:\n'
                             'valid example: maze.txt')
        else:
            return file_name

    @model_validator(mode='after')
    def validator_maze(self):
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT
        if entry_x >= self.WIDTH or exit_x >= self.WIDTH:
            raise ValueError('Coordinates cannot exceed Width')
        if entry_x < 0 or exit_x < 0:
            raise ValueError('Coordinates cannot be negative')
        if entry_y >= self.HEIGHT or exit_y >= self.HEIGHT:
            raise ValueError('Coordinates cannot exceed Height')
        if entry_y < 0 or exit_y < 0:
            raise ValueError('Coordinates cannot be negative')
        if self.ENTRY == self.EXIT:
            raise ValueError('Entry and Exit cannot be the same cell')
        return self
