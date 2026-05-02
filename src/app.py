"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""

from .parser import load_settings
from .classes import Settings, Maze


def run(settings: Settings) -> None:

    while (True):
        print("""
            === A-Maze-ing ===

            1. Show settings
            2. Read new settings
            3. Generate maze
            4. Show maze
            0. Exit
            """)
        match input("Select option: ").strip():
            case "1":
                print(settings)
            case "2":
                settings = load_settings("config.txt")
            case "3":
                maze = Maze(settings)
                print("Maze generated")
            case "4":
                if maze is None:
                    print("Generate a maze first")
                else:
                    print(maze)
            case "0":
                break
            case _:
                print("Invalid option")
