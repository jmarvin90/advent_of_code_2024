

import time
import itertools
from grid import Point, Grid

my_grid = Grid("puzzle_6_input_2.txt")

directions = [
    {
        "char": "^", 
        "vector": Point(0, -1),
        "path_char": "|"
    },
    {
        "char": ">", 
        "vector": Point(1, 0),
        "path_char": "-"
    },
    {
        "char": "V", 
        "vector": Point(0, 1),
        "path_char": "|"
    },
    {
        "char": "<", 
        "vector": Point(-1, 0),
        "path_char": "-"
    }
]

obstructions = ["#"]


def get_next_direction(current_char: str) -> Point:
    for index, direction in enumerate(directions):
        if direction["char"] == current_char:
            return directions[(index + 1) % len(directions)]


def get_path(grid: Grid, current_pos: Point, direction: Point) -> list:
    """Return a path ending at the next obstacle/end of the grid."""
    path = []
    while True:        
        path.append(current_pos)
        next_pos = current_pos + direction

        if (
            grid.at(current_pos) in obstructions or
            not next_pos.is_valid(grid)
        ):
            break

        current_pos = next_pos
    return path

"""
    A point on the grid "closes a loop" if:
    - we come to a point whose right adjacent point has been traversed already, and
    - we turn right onto that already traversed point, and
    - the subsequent path terminates in an obstacle
"""


def patrol(grid: Grid, start_point: Point, direction: dict) -> Grid:
    """Mark patrol paths on a grid from a specified start point."""

    current_pos = start_point
    current_direction = direction

    path = get_path(grid, current_pos, current_direction["vector"])

    while path:

        next_pos = path.pop(0)
        next_direction = get_next_direction(current_direction["char"])

        # Change directions if we're obstructed
        if grid.at(next_pos) in obstructions:
            current_direction = next_direction
            path = get_path(grid, current_pos, current_direction["vector"])
            continue
        
        current_pos = next_pos

        # Leave a breadcrumb indicating direction if we've not been here before
        if grid.at(current_pos) not in ["-", "|", "+"]:
            grid.set(current_pos, current_direction["path_char"])

        # Use a special breadcrumb if we've crossed the point in many directions
        if (
            grid.at(current_pos) in ["-", "|"] and 
            grid.at(current_pos) != current_direction["path_char"]
        ):
            grid.set(current_pos, "+")

        print(grid, end="\n\n")
        time.sleep(0.05)
    return grid

start_direction = directions[0]
start_point = my_grid.match_one(start_direction["char"])
output_grid = patrol(my_grid, start_point, start_direction)
