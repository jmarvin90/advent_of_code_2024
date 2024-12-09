

import cProfile
import time
import copy
import itertools
from grid import Point, Grid, Line

my_grid = Grid("puzzle_6_input.txt", obstructions={"#"})

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


def get_path(
    start_point: Point, 
    direction: Point, 
    grid: Grid,
    obstruction_points: set
) -> Line:
    """Follow the direction from the start point to a boundary/obstacle."""
    current_point = start_point

    while True:
        next_point = current_point + direction

        if (not next_point.is_valid(grid)):
            break

        if (next_point in obstruction_points):
            break

        current_point = next_point

    return Line(start_point, current_point)
        

def traverse_from(
    start_point: Point, 
    direction: Point, 
    grid: Grid, 
    additional_obstruction: Point | None = None
) -> set:
    """Follow a series of paths until we leave the grid."""
    current_point = start_point
    current_direction = direction

    path=set()

    obstruction_points = grid.obstruction_points

    if additional_obstruction is not None:
        obstruction_points = {*obstruction_points, additional_obstruction}

    while True:
        next_leg = get_path(
            current_point, current_direction, grid, obstruction_points
        )

        if next_leg in path:
            raise RecursionError("I've been there before...")

        path = {*path, next_leg}
        next_leg_termination_point = next_leg.end_point + current_direction

        if not next_leg_termination_point.is_valid(grid):
            break
        
        if (next_leg_termination_point in obstruction_points):
            current_point = next_leg.end_point
            current_direction = get_next_direction(current_direction)

    return path


def get_closure_points(
    path: set, grid: Grid, start_point: Point, start_direction: Point
) -> set:
    closures = {}

    for move in path:
        for point in move.points:
            closure_point = point + move.direction
            if closure_point != start_point:
                try:
                    traverse_from(
                        start_point,
                        start_direction,
                        my_grid, additional_obstruction=closure_point
                    )
                except RecursionError:
                    closures = {*closures, closure_point}
    return closures



start_point = my_grid.match_one("^")
start_direction = Point(0, -1)
points = set()

# cProfile.run("traverse_from(start_point, start_direction, my_grid)")
output_paths = traverse_from(start_point, start_direction, my_grid)

for path in output_paths:
    points = points | path.points

print(len(points))

closures = get_closure_points(output_paths, my_grid, start_point, start_direction)
print(len(closures))

