"""
Parser Module
=============
Parses and validates config.txt

Expects:
    file_name: str

Returns:
    Settings: validated settings from config.txt
"""
from sys import argv
from typing import Any
from .classes import Settings, Maze
try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def main() -> None:

    if len(argv) == 2:
        print("\nValidating settings and starting Maze generator:")
        settings: Settings | None = load_settings(argv[1], "init")
        if settings is None:
            print("Error settings")
    else:
        print("Invalid argument count\nUsage: "
              "python3 a-maze-ing.py config.txt")
    print()


def load_settings(source: str, flag: str) -> Settings:
    """ Parsing and settings loader handler """
    from .app import run

    try:

        if flag == "init":
            settings: Settings = settings_parser(source)
            maze: Maze = Maze(settings)
            maze.generate()
            run(settings, maze)
        elif flag == "run":
            settings = settings_parser(source)
        return (settings)

    except ValidationError as error:
        for _error in error.errors():
            if _error['loc']:
                print(f"Error location: {_error['loc'][0]} (config.txt)")
            print(f"Error message: {_error['msg']}")
    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
    ) as file_error:
        print(f"\nFile error: {file_error}")
        exit(1)
    except ValueError as value_error:
        print(f"\nError message: {value_error}")
        exit(1)
    except (Exception, BaseException) as exceptional_error:
        print(f"\nUnexpected Error: {exceptional_error}")
        exit(1)
    return settings


def settings_parser(file_name: str) -> Settings:
    """ Settings parser """

    parsed_settings: dict[str, Any] = {}

    with open(file_name, 'r') as config_file:
        _settings: list[str] = config_file.read().split('\n')

    for line in _settings:
        setting: str = line.strip()
        if not setting or setting.startswith("#"):
            continue
        if "=" not in setting:
            raise ValueError(f"{setting} missing '=' sign")
        else:
            key, value = setting.split('=', 1)
            parsed_settings[key.upper()] = value.strip()

    if not all(key.isidentifier() for key in parsed_settings.keys()):
        raise ValueError("Invalid key format in config file")

    settings: Settings = Settings(**parsed_settings)
    return settings
