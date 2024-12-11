import pathlib
from grid import Grid, Line
import itertools

my_grid = Grid("puzzle_input_8_2.txt")
antenna_types = {value for value in my_grid.distinct_vals if value != "."}

def get_antinodes(grid: Grid, repeat: bool=False) -> set:
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
        
    return antinodes

print(len(get_antinodes(my_grid)))

        