from __future__ import annotations
import functools
import itertools
import pathlib
import math

class Grid:
    """Some helpful grid functionality."""
    def __init__(self, input_file: str, obstructions: set=set()):
        self.input_file = input_file
        self.grid = Grid.from_input_file(self.input_file)
        self.obstructions = obstructions

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)

    @staticmethod
    def from_input_file(input_file) -> list:
        grid = []
        with pathlib.Path(input_file).open("r") as in_file:
            for line in in_file:
                grid.append(list(line.strip('\n')))
        return grid

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def height(self):
        return len(self.grid)

    def at(self, point: Point) -> str:
        return self.grid[point.y][point.x]

    def match(self, value: str) -> list:
        return [
            Point(x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val == value
        ]

    def match_one(self, value: str) -> str:
        return self.match(value)[0]

    def match_any(self, values: list) -> list:
        return [
            Point(x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val in values
        ]

    def count(self, value:str) -> list:
        return len(self.match(value))

    def count_any(self, values: list) -> list:
        return len(self.match_any(values))

    def set(self, point: Point, char: str) -> None:
        self.grid[point.y][point.x] = char

    @functools.cached_property
    def obstruction_points(self) -> set:
        return self.match_any(self.obstructions)

    @functools.cached_property
    def distinct_vals(self) -> set:
        vals = set()
        for row in self.grid:
            vals = vals | set(row)
        return vals


class Point:
    """Some helpful point functionality."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self) -> str:
        return hash((self.__str__()))

    def __eq__(self, comparator: Point) -> bool:
        return self.x == comparator.x and self.y == comparator.y

    def __str__(self) -> str:
        return f"{self.x},{self.y}"
    
    def __add__(self, point: Point) -> Point:
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point: Point) -> Point:
        return Point(self.x - point.x, self.y - point.y)

    def __neg__(self) -> Point:
        return Point(self.x * -1, self.y * -1)

    def __mul__(self, num_: int) -> Point:
        return Point(self.x * num_, self.y * num_)

    def is_valid(self, grid: Grid) -> bool:
        return (
            grid.width > self.x >= 0 and
            grid.height > self.y >= 0
        )
    
    def is_on_boundary(self, grid: Grid) -> bool:
        return (
            (self.x == 0 or self.x == grid.width -1) or
            (self.y == 0 or self.y == grid.height -1)
        )

    def distance_to(self, point: Point) -> float:
        line = Line(self, point)
        return math.hypot(
            line.x_diff, line.y_diff
        )


class Line:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point

    def __str__(self) -> str:
        return f"{str(self.start_point)} -> {str(self.end_point)}"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, comparator: Line) -> bool:
        return (
            comparator.start_point == self.start_point and
            comparator.end_point == self.end_point
        )

    @functools.cached_property
    def x_diff(self) -> int:
        return self.start_point.x - self.end_point.x

    @functools.cached_property
    def y_diff(self) -> int:
        return self.start_point.y - self.end_point.y

    @functools.cached_property
    def diff(self) -> Point:
        return Point(self.x_diff, self.y_diff)

    @functools.cached_property
    def is_horizontal(self) -> bool:
        return self.start_point.y == self.end_point.y

    @functools.cached_property
    def is_vertical(self) -> bool:
        return self.start_point.x == self.end_point.x

    @functools.cached_property
    def direction(self) -> Point:
        # Horizontal
        if self.is_horizontal:
            return (
                Point(1 if self.start_point.x < self.end_point.x else -1, 0)
            )

        # Vertical
        if self.is_vertical:
            return (
                Point(0, 1 if self.start_point.y < self.end_point.y else -1)
            )

        return self.diff

    @functools.cached_property
    def points(self) -> set:
        if self.is_horizontal:
            return {
                Point(number, self.start_point.y)
                for number in range(
                    self.start_point.x,
                    self.end_point.x + self.direction.x,
                    self.direction.x
                )
            }

        return {
            Point(self.start_point.x, number)
            for number in range(
                self.start_point.y,
                self.end_point.y + self.direction.y,
                self.direction.y
            )
        }
