# A-Maze-ing

---

## Description

A-Maze-ing is a Python maze generator that procedurally creates fully connected, solvable mazes using a Depth-First Search (DFS) algorithm. The program supports graphical display, step-through visualization, seed-based reproducibility, and configuration via a settings file.

---

## Instructions

### Requirements

- Python 3.x
- pip
- pydantic
- flake8
- mypy

### Installation

```bash
git clone git@github.com:Diogo-Serra/A-Maze-ing.git
cd A-Maze-ing
pip install -r requirements.txt
```

### Execution

Run with a seed (optional):
```bash
python a-maze-ing.py [seed]
```

Run with a settings file:
```bash
python a-maze-ing.py settings.txt
```

---

## Settings File Format

The settings file must follow this structure:

```
WIDTH=int
HEIGHT=int
ENTRY=tuple
EXIT=tuple
OUTPUT_FILE=maze.txt
PERFECT=bool
```

All fields are required.

---

## Maze Generation Algorithm

The maze is generated using a **Depth-First Search (DFS)** algorithm with recursive backtracking:

1. Start at a random cell and mark it as visited.
2. Randomly choose an unvisited neighbouring cell, carve a passage to it, and move there.
3. If no unvisited neighbours exist, backtrack to the previous cell.
4. Repeat until all cells have been visited.

This guarantees a fully connected, solvable maze with exactly one path between any two cells.

### Why DFS?

We chose DFS because it is simple to implement, produces long winding corridors (visually interesting and challenging), and guarantees a perfect maze (no loops and no isolated regions). Its recursive nature also maps naturally to Python. This algorithm can still be revisited and changed.

---

## Reusable Components

- **Maze generator module** (`maze.py`) - The core DFS logic is decoupled from the display layer and can be reused in any project that needs maze generation. The `Maze` class also validates input data and supports maze creation directly from a settings file.
- **Settings parser** - The config reader can be reused in other projects that require strict file-based configuration and validation.

---

## Team & Project Management

### Roles

| Member | Role |
|---|---|
| [Diogo Serra](https://github.com/Diogo-Serra) | Settings parser, input validation, testing
| [Pedro Pinhão](https://github.com/Retr02k) | Core algorithm, graphical display, testing

### Planning

Initial planned timeline:

- Week 1: project setup and algorithm research
- Week 2: settings parsing, game flow, and menus
- Week 3: core maze generation
- Week 4: graphical display and visualization

### What Worked Well & What Could Be Improved

**Worked well:**
    ...

**Could be improved:**
    ...

### Tools Used

- **Version Control**: Git, GitHub
- **Core Development**: Python, pip, venv
- **Validation & Quality**: pydantic, flake8, mypy
- **Environment & Editor**: Linux, VS Code
- **Shells**: bash, zsh

---

## Resources

- DFS maze generation: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Python `random` module: https://docs.python.org/3/library/random.html
- Python documentation: https://docs.python.org/3/
- Pydantic documentation: https://docs.pydantic.dev/
- pip documentation: https://pip.pypa.io/en/stable/
- flake8 documentation: https://flake8.pycqa.org/
- W3Schools Python references: https://www.w3schools.com/python/
- GeeksforGeeks DFS references: https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

### AI Usage

AI tools were used for research support, concept clarification, and creating visual explanations to better understand maze generation logic.

No code was generated with AI; implementation, decisions and code were written by us.

