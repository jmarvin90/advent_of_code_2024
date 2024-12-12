import pathlib
from grid import Grid, Line
import itertools

my_grid = Grid("puzzle_input_8.txt")
antenna_types = {value for value in my_grid.distinct_vals if value != "."}


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

        # Double the size of the line from the centre point
        extended_lines = [
            Line(
                line.start_point + line.diff,
                line.end_point - line.diff
            ) for line in lines
        ]

        # Add the new start and end points to the antinodes set
        antinodes = {
            *antinodes, 
            *[
                point 
                for line in extended_lines 
                for point in [line.start_point, line.end_point]
                if point.is_valid(grid)
            ]
        }
        
    return antinodes

print(len(get_antinodes(my_grid)))

        