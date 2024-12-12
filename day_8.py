import pathlib
from grid import Grid, Line, Point
import itertools

my_grid = Grid("puzzle_input_8.txt")
antenna_types = {value for value in my_grid.distinct_vals if value != "."}

def step(start_point: Point, direction: Point, grid: Grid) -> set:
    next_step = start_point + direction
    if next_step.is_valid(grid):
        return {start_point, next_step, *step(next_step, direction, grid)}
    else:
        return {start_point}

def get_antinodes(grid: Grid) -> set:
    antinodes = set()

    print(f"Grid height: {grid.height}; grid width: {grid.width}")

    # For each type of antenna
    for antenna_type in antenna_types:
        # Get the set of locations
        antennas = my_grid.match_any(antenna_type)

        # And create line between all pairwise combinations of locations
        lines = [
            Line(*pair) 
            for pair in itertools.combinations(antennas, 2)
        ]

        for line in lines:
            forwards = step(line.start_point, line.diff, grid)
            backwards = step(line.end_point, -line.diff, grid)

            antinodes = {
                *antinodes, 
                *forwards, 
                *backwards
            }

    return antinodes

print(len(get_antinodes(my_grid)))

        