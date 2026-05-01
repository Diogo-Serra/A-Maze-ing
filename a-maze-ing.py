"""
Entry point for the A-Maze-ing project

Usage:
    python3 main.py config.txt

Flow:
    1. Parse settings from config.txt -> dict
    2. Validate data with pydantic
    3. On success, Maze class is instantiated
"""


try:
    from sys import argv, exit
    from src import load_settings
except ImportError as error:
    print(error)
    exit(1)


def main() -> None:

    """ Main function - Maze Caller/Tester """

    load_settings(argv)


if __name__ == "__main__":
    main()
