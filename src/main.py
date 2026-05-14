from .parser import load_settings
from sys import argv


def main() -> None:

    if len(argv) == 2:
        print("\nValidating settings and starting Maze generator:")
        load_settings(argv[1], "init")
    else:
        print("Invalid argument count\nUsage: "
              "python3 a-maze-ing.py config.txt")

    print()
