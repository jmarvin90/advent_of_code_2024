

import time
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


"""
 - If instead of carrying on the current path, we took the next direction...
 - ...and there is an obstruction along the path in the next direction...
 - ...and we have already visited a tile along the path in the next direction,
      between the current position and the obstruction
"""

def patrol(grid: Grid, start_point: Point) -> Grid:

    current_pos = start_point

    for direction in directions:
        if direction["char"] == grid.at(current_pos):
            current_direction = direction

    while True:
        next_pos = current_pos + current_direction["vector"]

        if grid.at(current_pos) not in ["-", "|", "+"]:
            grid.set(current_pos, current_direction["path_char"])

        if (
            grid.at(current_pos) in ["-", "|"] and 
            grid.at(current_pos) != current_direction["path_char"]
        ):
            grid.set(current_pos, "+")

        if not next_pos.is_valid(grid):
            break

        if grid.at(next_pos) in obstructions:
            current_direction = get_next_direction(current_direction["char"])
            continue

        current_pos = next_pos

    print(grid)
    return grid

output_grid = patrol(my_grid, my_grid.match_one("^"))
move_count = output_grid.count_any(["+", "-", "|"])
print(move_count)
