from random import Random
from .settings import Settings


class MazeGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings
        self.WIDTH: int = settings.WIDTH
        self.HEIGHT: int = settings.HEIGHT
        self.ENTRY: tuple[int, int] = settings.ENTRY
        self.EXIT: tuple[int, int] = settings.EXIT
        self.OUTPUT_FILE: str = settings.OUTPUT_FILE
        self.PERFECT: bool = settings.PERFECT
        self.SEED: int | None = settings.SEED
        self.grid: list[list[int]] | None = None
        self.fixed: set[tuple[int, int]] = set()

    def show_maze(self) -> None:
        if self.grid is None:
            raise ValueError("Generate a maze first")
        grid: list[list[int]] = self.grid
        print("Generated maze:\n")
        print('\n'.join(
             ''.join(format(cell, 'X') for cell in row)
             for row in grid)
        )
        print()

    def save_maze(self) -> None:
        if self.grid is None:
            raise ValueError("Generate a maze first")
        with open("Output_" + self.settings.OUTPUT_FILE, 'w') as f:
            for row in self.grid:
                f.write(''.join(format(cell, 'X') for cell in row) + '\n')
            f.write('\n')
            f.write(f'{self.ENTRY}\n')
            f.write(f'{self.EXIT}\n')
            f.write("Pathfinder\n")

    def generate(self) -> None:
        NORTH = 0x1
        EAST = 0x2
        SOUTH = 0x4
        WEST = 0x8

        DIRECTIONS = {
            NORTH: (0, -1),
            EAST:  (1,  0),
            SOUTH: (0,  1),
            WEST:  (-1, 0)}

        OPPOSITE = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST:  WEST,
            WEST:  EAST}

        rng = Random(self.SEED)

        FOUR = [
            [1, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]
        TWO = [
            [1, 1, 1],
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
            [1, 1, 1],
        ]
        PATTERN_W = 7
        PATTERN_H = 5

        # Fixed cells if the maze is large enough (min 9x7)
        self.fixed = set()
        if self.WIDTH >= PATTERN_W + 2 and self.HEIGHT >= PATTERN_H + 2:
            start_x = (self.WIDTH - PATTERN_W) // 2
            start_y = (self.HEIGHT - PATTERN_H) // 2
            for row in range(PATTERN_H):
                for col in range(3):
                    if FOUR[row][col]:
                        self.fixed.add((start_x + col, start_y + row))
                    if TWO[row][col]:
                        self.fixed.add((start_x + 4 + col, start_y + row))
        else:
            print("Note: Maze too small for the '42' pattern, omitting it.")

        # 1. Start: Fill grid with 0xF
        self.grid = [
            [0xF] * self.WIDTH for _ in range(self.HEIGHT)]

        # 2. DFS — fixed cells are pre-visited so DFS never carves them
        visited: set[tuple[int, int]] = set(self.fixed)
        stack: list[tuple[int, int]] = [self.ENTRY]
        visited.add(self.ENTRY)

        while stack:
            x, y = stack[-1]
            dirs = list(DIRECTIONS.keys())
            rng.shuffle(dirs)
            carved = False
            for direction in dirs:
                dx, dy = DIRECTIONS[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.WIDTH and 0 <= ny < self.HEIGHT:
                    if (nx, ny) not in visited:
                        self.grid[y][x] &= ~direction
                        self.grid[ny][nx] &= ~OPPOSITE[direction]
                        visited.add((nx, ny))
                        stack.append((nx, ny))
                        carved = True
                        break
            if not carved:
                stack.pop()

        # 3. If perfect=false, remove extra walls (skip fixed cells)
        if not self.PERFECT:
            for _ in range(self.WIDTH * self.HEIGHT // 4):
                x = rng.randint(0, self.WIDTH - 2)
                y = rng.randint(0, self.HEIGHT - 2)
                direction = rng.choice([EAST, SOUTH])
                dx, dy = DIRECTIONS[direction]
                nx, ny = x + dx, y + dy
                if (x, y) not in self.fixed and (nx, ny) not in self.fixed:
                    self.grid[y][x] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSITE[direction]

        self.save_maze()

    def render_maze(self, color: str) -> None:
        if self.grid is None:
            return

        NORTH = 0x1
        WEST = 0x8

        RESET = "\033[0m"
        YELLOW_BG = "\033[43m"
        MAIN = "\033[94m" if color == "blue" else ""

        grid = self.grid
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0
        fixed = self.fixed

        output = []

        for y in range(height):
            # Top wall row
            top = MAIN
            for x in range(width):
                cell = grid[y][x]
                top += "+" + ("---" if (cell & NORTH) else "   ")
            output.append(top + "+" + (RESET if MAIN else ""))

            # Cell row with left walls
            mid = ""
            for x in range(width):
                cell = grid[y][x]
                wall = MAIN + ("|" if (cell & WEST) else " ") + RESET
                if (x, y) in fixed:
                    interior = YELLOW_BG + "   " + RESET
                elif (x, y) == self.ENTRY:
                    interior = MAIN + " S " + (RESET if MAIN else "")
                elif (x, y) == self.EXIT:
                    interior = MAIN + " E " + (RESET if MAIN else "")
                else:
                    interior = MAIN + "   " + (RESET if MAIN else "")
                mid += wall + interior
            output.append(mid + MAIN + "|" + (RESET if MAIN else ""))

        # Bottom border
        output.append(MAIN + "+" + "---+" * width + (RESET if MAIN else ""))

        print()
        print('\n'.join(output))
        print()
