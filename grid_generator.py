from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from random import randint
from typing import List, TypeAlias
import time


class Element(Enum):
    EMPTY = auto()
    BLOCK = auto()


@dataclass
class Coord:
    x: int
    y: int


Grid: TypeAlias = List[List[Element]]


class GridGenerator:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        obstacles: int = 1,
        start: Coord = Coord(0, 0),
        goal: Coord = Coord(10, 10),
    ) -> None:
        self.rows_ = rows
        self.columns_ = columns
        self.obstacles_ = obstacles
        self.start_ = start
        self.goal_ = goal

    def new(self) -> Grid:
        grid = [
            [Element.EMPTY for _ in range(self.columns_)] for _ in range(self.rows_)
        ]

        for _ in range(self.obstacles_):
            while True:
                x, y = randint(0, self.rows_ - 1), randint(0, self.columns_ - 1)
                if (x, y) != (self.start.x, self.start.y) and (x, y) != (
                    self.goal.x,
                    self.goal.y,
                ):
                    grid[x][y] = Element.BLOCK
                    break

        # Set start and goal points
        grid[self.start.x][self.start.y] = Element.EMPTY
        grid[self.goal.x][self.goal.y] = Element.EMPTY

        return grid

    def new_mock() -> Grid:
        return [
            [Element.BLOCK if character == "#" else Element.EMPTY for character in line]
            for line in Path("fake_grid").read_text("utf-8").strip().split("\n")
        ]

    def is_path_available(self, grid: Grid) -> bool:
        attempts = 0
        start_time = time.time()

        while attempts < 5:
            if time.time() - start_time > 5:  # Timeout after 5 seconds
                return False

            if self._breadth_first_search(grid, self.start_, self.goal_):
                return True

            # If path not found, modify grid and retry
            self._modify_grid(grid)
            attempts += 1

        return False

    def _breadth_first_search(self, grid: Grid, start: Coord, goal: Coord) -> bool:
        directions = [
            (0, -1),  # SOUTH
            (0, 1),  # NORTH
            (-1, 0),  # WEST
            (1, 0),  # EAST
        ]
        rows = len(grid)
        columns = len(grid.at(0))

        visited = set()
        visited.add((start.x, start.y))

        queue = deque([(start.x, start.y)])

        while queue:
            x, y = queue.popleft()

            if (x, y) == (goal.x, goal.y):
                return True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < columns
                    and (nx, ny) not in visited
                    and grid[nx][ny] != Element.BLOCK
                ):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return False
