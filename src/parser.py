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


from sys import exit
from string import punctuation, digits
from .classes import Settings, ValidationError


def load_settings(argv: list[str]) -> dict:
    """ Parsing and settings loader handler """

    try:
        validated_argv: dict[str, str] = argv_parser(argv)
        setting_file: str = validated_argv['config']
    except ValueError as error:
        print(error)
        exit(1)

    try:
        settings: Settings = settings_parser(setting_file)
        print(settings)
    except ValidationError as e:
        for error in e.errors():
            print(error['loc'])
            print(error['msg'])


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

    settings: dict[str, int | float | bool] = {}

    try:
        with open(file_name, 'r') as config_file:
            _settings: str = config_file.read().split('\n')
    except (FileNotFoundError, FileExistsError) as error:
        print(error)
        exit(1)

    for line in _settings:
        setting = line.strip()
        if "=" not in setting:
            raise ValueError(f"{setting} missing '=' sign")
        else:
            key, value = setting.split('=')
            settings[key] = value

    try:
        if not all(key.isidentifier() for key in settings.keys()):
            raise ValueError("Only alphabetic keys in config file")
        for key in settings.keys():
            key.upper()
    except ValueError as error:
        print(error)
        exit(1)

    x, y = settings['ENTRY'].split(",")
    print(y)

    try:
        settings = Settings(**settings)
    except ValidationError as error:
        for error in error.errors():
            print(error['loc'][0])
            print(error['msg'])
            exit(1)

    return settings
