"""
Entry point for the A-Maze-ing project

Usage:
    python3 main.py config.txt

Flow:
    1. Parse settings from config.txt -> dict
    2. Validate data with pydantic
    3. On success, Maze class is instantiated
"""

from sys import argv
from src import load_settings, Settings, run


def main() -> None:

    """ Main function - Maze Caller/Tester """
    if len(argv) == 2:
        print("\nValidating settings: ")
        settings: Settings = load_settings(argv)
        if settings:
            print("Success validating config.txt")
            print("Starting now ...")
    else:
        print("Invalid argument count\nUsage: "
              "python3 main.py config.txt")
    print()

    run(settings)


if __name__ == "__main__":
    main()
