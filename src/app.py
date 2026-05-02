"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""

from .parser import load_settings
from .classes import Settings, Maze


def run(settings: Settings, maze: Maze) -> None:

    while (True):

        print("""
            === A-Maze-ing ===

            1. Show settings
            2. Read new settings
            3. Generate a Maze grid
            4. TODO: Visualizer active maze (Maze method)
            0. Exit
            """)

        match input("Select option: ").strip():
            case "1":
                print(settings)
            case "2":
                old_settings: Settings = settings
                settings, maze = load_settings("config.txt")
                if old_settings == settings:
                    print("No changes from previous read")
                else:
                    print("Success reading new config.txt")
                    print("New settings updated!")
            case "3":
                maze.generate()
                print(maze)
            case "0":
                break
            case _:
                print("Invalid option")
