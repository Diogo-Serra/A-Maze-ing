"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""
from os import system, name
from .parser import load_settings
from .classes import Settings, Maze


def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


def wait_input() -> None:
    input('Press any key to continue ...')


def run(settings: Settings, maze: Maze) -> None:

    while (True):
        clear_screen()
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
                clear_screen()
                settings.show_settings()
                wait_input()
            case "2":
                clear_screen()
                old_settings: Settings = settings
                settings, maze = load_settings("config.txt")
                if old_settings == settings:
                    print("No changes from previous read")
                else:
                    print("Success reading new config.txt")
                    print("New settings updated!")
                wait_input()
            case "3":
                clear_screen()
                maze.generate()
                maze.show_maze()
                wait_input()
            case "0":
                print("Exiting now. Closing program.")
                break
            case _:
                print("Invalid option")
                wait_input()
