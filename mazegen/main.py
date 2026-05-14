"""Main module - entry point for the A-Maze-ing application."""
from .parser import load_settings
from sys import argv


def main() -> None:
    """Parses command-line arguments and starts the maze generator."""

    if len(argv) == 2:
        print("\nValidating settings and starting Maze generator:\n")
        load_settings(argv[0], argv[1], "init")
    else:
        print("Invalid argument count\nUsage: "
              "python3 a-maze-ing.py config.txt")

    print()
