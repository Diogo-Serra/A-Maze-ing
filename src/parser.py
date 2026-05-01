"""
Parses and validates [argv, config.txt]

Expects:
    argv: list[str]

Returns:
    dict: validated settings from config.txt

Raises:
    SystemExit: if argv is invalid or config file are not found
"""


try:
    from sys import exit
    from typing import Any
    from string import punctuation, digits
except ImportError as error:
    print(error)
    exit(1)


def load_settings(argv: list[str]) -> dict:

    try:
        validated_argv: dict[str, str] = argv_parser(argv)
        print(validated_argv)
    except ValueError as error:
        print(error)
        exit(1)


def argv_parser(argv: list[str]) -> dict[str, str]:

    usage: list[str] = ["a-maze-ing.py", "config.txt"]

    if len(argv) == 2:
        script: str = argv[0].strip(punctuation + digits + " ")
        config: str = argv[1].strip(punctuation + digits + " ")
        if not all(x in usage for x in [script, config]):
            raise ValueError("Incorrect input\nUsage: "
                  "python3 a-maze-ing.py config.txt")
        return {'script': script, 'config': config}
    else:
        raise ValueError("Incorrect input\n"
                         "Usage: python3 a-maze-ing.py config.txt")


def settings_parser(file_name: str) -> dict[str, Any]:
    pass
