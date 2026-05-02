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

    maze: Maze = None

    while (True):
        print("""
            === A-Maze-ing ===

            1. Show settings
            2. Read new settings
            3. Create maze class
            4. Show active Maze instance
            5. TODO: Generate new maze (Maze method)
            6. TODO: Output active maze (Maze method)
            7. TODO: Visualizer active maze (Maze method)
            0. Exit
            """)
        match input("Select option: ").strip():
            case "1":
                print(settings)
            case "2":
                new_settings: Settings = settings
                settings = load_settings("config.txt")
                if new_settings == settings:
                    print("No changes from previous")
                else:
                    print("Success reading new config.txt")
                    print("New settings updated!")
            case "3":
                maze = Maze(settings)
                print("Maze class generated")
            case "4":
                if maze is None:
                    print("Generate a maze first")
                else:
                    print(maze)
                    print("Success creating new Maze class")
            case "0":
                break
            case _:
                print("Invalid option")
