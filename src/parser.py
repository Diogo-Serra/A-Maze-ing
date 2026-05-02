"""
Parser Module
=============
Parses and validates [argv, config.txt].

Expects:
    argv: list[str]

Returns:
    Settings: validated settings from config.txt

Raises:
    SystemExit: if argv is invalid or config file not found
"""


from typing import Any
from .classes import Settings
from string import punctuation, digits


try:
    from pydantic import ValidationError
except ImportError as error:
    print(error)


def load_settings(argv: list[str]) -> Settings:
    """ Parsing and settings loader handler """

    try:

        validated_argv: dict[str, str] = argv_parser(argv)
        setting_file: str = validated_argv['config']
        settings_class: Settings = settings_parser(setting_file)

    except ValueError as error:
        print(error)
        exit(1)
    except ValidationError as error:
        for _error in error.errors():
            print(_error['loc'][0])
            print(_error['msg'])
            exit(1)
    except Exception as error:
        print(error)
        exit(1)

    return settings_class


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
