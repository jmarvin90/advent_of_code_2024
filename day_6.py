

import time
import itertools
from grid import Point, Grid

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


def traverse_from(start_point: Point, direction: Point, grid: Grid) -> None:

    current_point = start_point
    path=[start_point]

    while True:
    
        # The next point we want to go to
        next_point = current_point + direction

        # If that point would exit the map
        if not next_point.is_valid(grid):
            break

        # If that point is an obstacle
        if grid.at(next_point) in obstructions:
            direction = get_next_direction(direction)
            continue

        # If we've been at that point more than twice[?]
        if (path.count(next_point) == 2):
            print(f"Been here ({next_point}) too many times, mate.")
            break

        current_point = next_point
        path.append(current_point)

    return path


"""
    A point on the grid "closes a loop" if:
    - we come to a point at which, were we to turn right...
    - ...the path we would traverse from that point would include a step we've
         already traversed before...
    - ...from the same direction that we're traversing this time...?
"""


output_path = traverse_from(my_grid.match_one("^"), Point(0, -1), my_grid)


print(len(set(output_path)))            # PT 1 - Answer
