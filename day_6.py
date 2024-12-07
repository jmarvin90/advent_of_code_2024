

import time
import itertools
from grid import Point, Grid, Line

my_grid = Grid("puzzle_6_input_2.txt")

directions = [
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0) 
]

obstructions = ["#"]

def get_next_direction(current_direction: Point) -> Point:
    for index, direction in enumerate(directions):
        if direction == current_direction:
            return directions[(index + 1) % len(directions)]


def get_path(start_point: Point, direction: Point, grid: Grid) -> list:
    """Follow the direction from the start point to a boundary/obstacle."""
    path = []
    current_point = start_point

    while True:
        next_point = current_point + direction
        path.append(Line(current_point, next_point))

        if (
            not next_point.is_valid(grid) or 
            grid.at(next_point) in obstructions
        ):
            break

        current_point = next_point

    return path
        

def traverse_from(
    start_point: Point, 
    direction: Point, 
    grid: Grid, 
    level: int=0
) -> None:

    current_point = start_point
    path=[]
    loop_closure_points = []

    while True:
    
        # The next point we want to go to
        next_point = current_point + direction
        next_direction = get_next_direction(direction)

        # If that point would exit the map
        if not next_point.is_valid(grid):
            break

        # If that point is an obstacle
        if grid.at(next_point) in obstructions:
            direction = get_next_direction(direction)
            continue

        # If we're observed this move before
        if Line(current_point, next_point) in path:
            raise RecursionError("This traversal appears to loop infinitely")
            break

        path.append(Line(current_point, next_point))
        current_point = next_point

    return path


test = get_path(Point(5, 6), Point(0, -1), my_grid)

for line in test:
    print(line, my_grid.at(line.end_point))