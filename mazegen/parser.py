"""
Parser Module
=============
Parses and validates script name and config.txt for settings

Expects:
    script_name: str - argv[0]
    file_name: str - argv[1]

Returns:
    Settings: validated settings from config.txt
"""
from typing import Any
from .mazegen import MazeGenerator, Settings
try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def load_settings(script_name: str, config_file: str, flag: str) -> Settings:
    """Central entry point for loading, validating and launching.

    Controls two execution flows via flag:
        'init' — startup: validates script name, parses config, builds the
                 maze and launches the interactive app. Exits on any error.
        'run'  — in-app reload: re-parses config.txt without restarting.

    Handles all error types: Pydantic ValidationError, file errors,
    value errors and unexpected exceptions.
    Usage: load_settings(argv[0], argv[1], 'init')"""
    from .app import run

    try:

        if flag == "init":
            if script_name.strip() != "a-maze-ing.py":
                raise ValueError(f"Invalid script name {script_name}."
                                 "\nScript name should be: a-maze-ing.py.")
            settings: Settings = settings_parser(config_file)
            maze: MazeGenerator = MazeGenerator(settings)
            maze.generate()
            run(settings, maze)
        elif flag == "run":
            settings = settings_parser(config_file)
        return (settings)

    except ValidationError as error:
        for _error in error.errors():
            if _error['loc']:
                print(f"Error location: {_error['loc'][0]} (config.txt).")
            print(f"Error message: {_error['msg']}.")
    except (
        FileNotFoundError,
        FileExistsError,
        PermissionError,
    ) as file_error:
        print(f"File error: {file_error}")
        exit(1)
    except ValueError as value_error:
        print(f"Error message: {value_error}")
        exit(1)
    except (Exception, BaseException) as exceptional_error:
        print(f"\nUnexpected Error: {exceptional_error}")
        exit(1)


def settings_parser(file_name: str) -> Settings:
    """Reads and parses a config file into a dict
       and returns a validated Settings object.
       Usage: settings_parser('config.txt')"""

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
