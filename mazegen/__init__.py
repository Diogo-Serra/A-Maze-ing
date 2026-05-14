"""
Mazegen package - maze generator using DFS.

Exposes MazeGenerator and Settings for standalone use,
and main() as the CLI entry point for the A-Maze-ing project.
"""
from .main import main
from .mazegen import MazeGenerator, Settings

__all__ = ['main', 'MazeGenerator', 'Settings']
