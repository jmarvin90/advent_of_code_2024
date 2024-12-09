

import cProfile
import time
import copy
import itertools
from grid import Point, Grid, Line

# 1655

obstructions=["#"]
my_grid = Grid("puzzle_6_input.txt")

directions = [
    Point(0, -1),
    Point(1, 0),
    Point(0, 1),
    Point(-1, 0) 
]

def get_next_direction(current_direction: Point) -> Point:
    for index, direction in enumerate(directions):
        if direction == current_direction:
            return directions[(index + 1) % len(directions)]


def get_path(start_point: Point, direction: Point, grid: Grid) -> Line:
    """Follow the direction from the start point to a boundary/obstacle."""
    current_point = start_point

    while True:
        next_point = current_point + direction

        if (not next_point.is_valid(grid)):
            break

        if grid.at(next_point) in obstructions:
            break

        current_point = next_point

    return Line(start_point, current_point)
        

def traverse_from(start_point: Point, direction: Point, grid: Grid) -> None:
    """Follow a series of paths until we leave the grid."""
    current_point = start_point
    path=[]
    pathset = set()

    while True:
        next_leg = get_path(current_point, direction, grid)
        path.append(next_leg)
        next_leg_termination_point = next_leg.end_point + next_leg.direction

        if not next_leg_termination_point.is_valid(grid):
            break
        
        if grid.at(next_leg_termination_point) in obstructions:
            current_point = next_leg.end_point
            direction = get_next_direction(direction)

    return path


def get_loop_closures(path: list, grid: Grid) -> list:
    points = []

    for move in path:
        alt_direction = get_next_direction(move.direction)
        alt_path = get_path(move.start_point, alt_direction, grid)

        if (
            alt_path[-1].end_point.is_valid(grid) and
            grid.at(alt_path[-1].end_point) in obstructions
        ):
            alt_grid = copy.deepcopy(grid)
            alt_grid.set(move.end_point, "#")

            try:
                traverse_from(grid.match_one("^"), Point(0, -1), alt_grid)

            except RecursionError:
                print(f"Closure! {move.end_point}")
                points.append(move.end_point)

    return points


start_point = my_grid.match_one("^")
start_direction = Point(0, -1)
points = set()

cProfile.run("traverse_from(start_point, start_direction, my_grid)")
output_paths = traverse_from(start_point, start_direction, my_grid)

for path in output_paths:
    points = points | path.points

print(len(points))