from __future__ import annotations
import pathlib
import itertools


# Some helpful grid functionality
class Grid:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.grid = Grid.from_input_file(self.input_file)

    @staticmethod
    def from_input_file(input_file) -> list:
        grid = []
        with pathlib.Path(input_file).open("r") as in_file:
            for line in in_file:
                grid.append(list(line.strip('\n')))
        return grid

    @property
    def width(self):
        return len(self.grid[0])

    @property
    def height(self):
        return len(self.grid)

    def at(self, point: Point) -> str:
        return self.grid[point.y][point.x]


# Some helpful point functionality
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"
    
    def __add__(self, point: Point) -> Point:
        return Point(self.x + point.x, self.y + point.y)

    def __mul__(self, num_: int) -> Point:
        return Point(self.x * num_, self.y * num_)

    def is_valid(self, grid: Grid) -> bool:
        return (
            grid.width > self.x >= 0 and
            grid.height > self.y >= 0
        )

    def grid_val(self, grid: Grid) -> str:
        return grid.at(self)


# Get the input grid
grid = Grid("puzzle_4_input.txt")


# ---- Day 4, PT 1---- #

# Possible directions the target could be oriented 
moves = [
    Point(*move)
    for move in itertools.product([-1, 0, 1], repeat=2) 
    if move != (0, 0)
]

# The target we're looking for
target = ["X", "M", "A", "S"]

# All the places the target could start from
start_points = [
    Point(x, y)
    for y, row in enumerate(grid.grid)
    for x, col in enumerate(row)
    if grid.at(Point(x, y)) == target[0]
]

# A word is valid if all the chars match the target at the same indexes
def word_is_valid(word: list, target: list) -> bool:
    return all(target[index] == word[index] for index, char in enumerate(word))

# The number of occurrences (the answer)
total = 0

for start_point in start_points:                                # Try all the start points
    for direction in moves:                                     # Try all directions from the start point
        word = []                                               # Keep track of the word we've got so far...
        viable = True                                           # ...and whether it's viable to continue in this direction...
        current_point = start_point                             # ...and how far along we've travelled
        while viable and len(word) < len(target):               # While the word we're forming in this direciton is valid
            word += grid.at(current_point)                      # Add the next letter to the word...
            current_point = current_point + direction           # ...and keep moving in this direction

            viable = (                                          # We can continue, so long as...
                word_is_valid(word, target) and                 # The word we've got so far is valid, and...
                current_point.is_valid(grid)                    # ...we can go in the same direction without exceeding limits
            )

            if word == target:                                  # If we've found our target...
                total += 1                                      # ...increment our total

print(total)



# ---- Day 4, PT 2---- #

# Possible directions the target(s) could be oriented - diagonals only
moves = [Point(-1, -1), Point(-1, 1)]

# We're trying to find the centre of the 'X' - the char. 'A'
start_points = [
    Point(x, y)
    for y, row in enumerate(grid.grid)
    for x, col in enumerate(row)
    if grid.at(Point(x, y)) == "A"
]

# The total number of occurrences (the answer)
x_mas_total = 0

for start_point in start_points:                                # Try all the start points
    subtot = 0                                                  # Keep track of how many lines crossing our start point are valid
    for move in moves:                                          # Try each of the lines (top left->bottom right, top right->bottom left)

        up = start_point + move                                 # Get the diagonal start point 
        down = start_point + (move * -1)                        # Get the diagonal end point

        if not(
            up.is_valid(grid) and down.is_valid(grid)           # If either of those points arent' valid...
        ):
            continue                                            # ...move on to another start point

        up_char = grid.at(start_point + move)                   # Get the character from the diagonal start
        down_char = grid.at(start_point + (move * -1))          # Get the character form the diagonal end

        if (                                                    # The diagonal is valid if...
            up_char in ["M", "S"] and                           # The start of the diagonal is "M" or "S"; and
            down_char in ["M", "S"] and                         # The end of the diagonal is "M" or "S"; and
            up_char != down_char                                # The start and end of the diagonal aren't the same
        ):
            subtot += 1                                         # Increment our subtotal if it's valid
    if subtot > 1:
        x_mas_total += 1                                        # Increment our grand total for each start point that is crossed twice

print(x_mas_total)