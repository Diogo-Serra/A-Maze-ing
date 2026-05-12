"""
App Module
==========
Application controller and user interface.

Func:
    App: maze creation and user interaction
"""
from os import system, name
from sys import argv
from .parser import load_settings
from .classes import Settings, Maze, Visualizer


def clear_screen() -> None:
    system('cls' if name == 'nt' else 'clear')


def wait_input() -> None:
    input('Press any key to continue ...')


def main() -> None:
    if len(argv) == 2:
        print("\nValidating settings and starting Maze generator:")
        settings, maze = load_settings(argv[1])
        run(settings, maze)
    else:
        print("Invalid argument count\nUsage: "
              "python3 a-maze-ing.py config.txt")
    print()


def run(settings: Settings, maze: Maze) -> None:

    color: str = "white"
    visualizer = Visualizer(maze, color)

    while (True):
        clear_screen()
        print("""
            === A-Maze-ing ===

            1. Show settings
            2. Read new settings
            3. Generate a Maze grid
            4. Visualizer for active maze
            5. Change colors on visualiser
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
                    visualizer = Visualizer(maze, color)
                wait_input()
            case "3":
                clear_screen()
                maze.generate()
                maze.show_maze()
                wait_input()
            case "4":
                clear_screen()
                visualizer.render_maze()
                wait_input()
            case "5":
                clear_screen()
                color = "blue" if color == "white" else "white"
                visualizer = Visualizer(maze, color)
                print(f"Visualizer color changed to: {color}")
                visualizer.render_maze()
                wait_input()
            case "0":
                print("Exiting now. Closing program.")
                break
            case _:
                print("Invalid option")
                wait_input()
