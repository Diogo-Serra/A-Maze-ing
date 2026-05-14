"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""
from os import system, name
from .settings import Settings
from .parser import load_settings
from .mazegen import MazeGenerator


def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


def run(settings: Settings, maze: MazeGenerator) -> None:

    MENU = """
        === A-Maze-ing ===

        1. Show settings
        2. Read new settings
        3. Generate a Maze grid
        4. Change colors on visualizer
        0. Exit
    """

    clear_screen()
    color: str = "white"

    while (True):
        choice = input(MENU + "\n    Select option: ").strip()

        if choice == "0":
            print("    Exiting now. Closing program.")
            break

        clear_screen()
        match choice:
            case "1":
                settings.show_settings()
            case "2":
                old_settings: Settings = settings
                new_settings = load_settings("config.txt", "run")
                if new_settings is None:
                    print("Settings unchanged due to config errors")
                elif old_settings != new_settings:
                    settings = new_settings
                    maze = MazeGenerator(new_settings)
                    maze.generate()
                    maze.render_maze(color)
                    print("Success reading new config.txt")
                    print("New settings updated!")
                else:
                    print("No changes from previous read")
            case "3":
                maze.generate()
                maze.render_maze(color)
            case "4":
                color = "blue" if color == "white" else "white"
                if maze.grid is None:
                    maze.generate()
                maze.render_maze(color)
                print(f"Visualizer color changed to: {color}")
                maze.render_maze(color)
            case _:
                print("Invalid option")
