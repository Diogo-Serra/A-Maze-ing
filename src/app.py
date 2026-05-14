"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""
from os import system, name
from .parser import load_settings
from .classes import Settings, MazeGenerator, Visualizer


def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


MENU = """
    === A-Maze-ing ===

    1. Show settings
    2. Read new settings
    3. Generate a Maze grid
    4. Change colors on visualizer
    0. Exit
"""


def run(settings: Settings, maze: MazeGenerator) -> None:

    color: str = "white"
    visualizer = Visualizer(maze, color)

    clear_screen()
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
                if old_settings != new_settings:
                    print("Success reading new config.txt")
                    print("New settings updated!")
                    maze = MazeGenerator(new_settings)
                    maze.generate()
                    visualizer = Visualizer(maze, color)
                    visualizer.render_maze()
                else:
                    print("    No changes from previous read")
            case "3":
                maze.generate()
                visualizer = Visualizer(maze, color)
                visualizer.render_maze()
            case "4":
                color = "blue" if color == "white" else "white"
                if maze.grid is None:
                    maze.generate()
                visualizer = Visualizer(maze, color)
                print(f"    Visualizer color changed to: {color}")
                visualizer.render_maze()
            case _:
                print("    Invalid option")
