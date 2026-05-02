"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""

from .classes import Settings, Maze


def run(settings: Settings) -> None:

    while (True):
        print("""
            === A-Maze-ing ===

            1. Show settings
            2. Generate maze
            3. Show maze
            0. Exit
            """)
        match input("Select option: ").strip():
            case "1":
                print(settings)
            case "2":
                maze = Maze(settings)
                print("Maze generated")
            case "3":
                if not maze:
                    print("Generate a maze first")
                print(maze)
            case "0":
                break
            case _:
                print("Invalid option")
