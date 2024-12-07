

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
        

def traverse_from(start_point: Point, direction: Point, grid: Grid) -> None:
    """Follow a series of paths until we leave the grid."""
    current_point = start_point
    path=[]

    while True:
        next_leg = get_path(current_point, direction, grid)
        path.extend(next_leg[:-1])

        if not next_leg[-1].end_point.is_valid(grid):
            break
        
        if grid.at(next_leg[-1].end_point) in obstructions:
            current_point = next_leg[-1].start_point
            direction = get_next_direction(direction)

    return path

output = traverse_from(Point(4, 6), Point(0, -1), my_grid)

points = []
for line in output:
    for point in line.points:
        if point not in points:
            points.append(point)

print(len(points))

