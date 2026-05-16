"""Main module - entry point for the A-Maze-ing application."""
from .parser import load_settings
from sys import argv


def main() -> None:
    """Package entry point that validates CLI args and delegates setup."""

    if len(argv) == 2:
        print("\nValidating settings and starting Maze generator:\n")
        load_settings(argv[0], argv[1], "init")
    else:
        print("Invalid argument count\nUsage: "
              "python3 a-maze-ing.py config.txt")

    print()
