"""
Parser Module
=============
Parses and validates [argv, config.txt].

Expects:
    argv: list[str]

Returns:
    Settings: validated settings from config.txt
"""

from typing import Any
from string import punctuation, digits
from .classes import Settings
try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)
    exit(1)


def load_settings(source: list[str] | str) -> Settings:
    """ Parsing and settings loader handler """

    try:

        if isinstance(source, list):
            validated_argv: dict[str, str] = argv_parser(source)
            settings_file: str = validated_argv['config']
            settings: Settings = settings_parser(settings_file)
        elif isinstance(source, str):
            settings = settings_parser(source)
        else:
            raise ValueError(f"Invalid source type: {type(source)}")

    except ValidationError as error:
        for _error in error.errors():
            if _error['loc']:
                print(f"Error location: {_error['loc'][0]} (config.txt)")
            print(f"Error message: {_error['msg']}")
            exit(1)
    except (
        FileNotFoundError,
        FileExistsError,
        OSError,
        PermissionError
    ) as error:
        print(f"File error: {error}")
        exit(1)
    except ValueError as error:
        print(f"Error message: {error}")
        exit(1)
    except Exception as error:
        print(f"Unexpected Error: {error}")
        exit(1)

    return settings


def argv_parser(argv: list[str]) -> dict[str, str]:
    """ Argv parser returns dictionary with script and config file """
    usage: list[str] = ["a-maze-ing.py", "config.txt"]

    if len(argv) == 2:
        script: str = argv[0].strip(punctuation + digits + " ")
        config: str = argv[1].strip(punctuation + digits + " ")
        if not all(x in usage for x in [script, config]):
            raise ValueError("Incorrect input\n"
                             f"Invalid arguments: '{script}' '{config}'\n"
                             "Usage: python3 main.py config.txt")
        return {'script': script, 'config': config}
    else:
        raise ValueError("Incorrect input\n"
                         f"Expected 2 arguments, got {len(argv)}\n"
                         "Usage: python3 main.py config.txt")


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
