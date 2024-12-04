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

    def match(self, value: str) -> list:
        return [
            Point(x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val == value
        ]


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


# A word is valid if all the chars match the target at the same index
def word_is_valid(word: list, target: list) -> bool:
    return target[:len(word)] == word


# How to count occurrences of a word conventionally
def count_words_in_grid(grid: Grid, target_word: list) -> int:
    # Possible directions the target could be oriented 
    directions = [
        Point(*move)
        for move in itertools.product([-1, 0, 1], repeat=2) 
        if move != (0, 0)
    ]

    # The places the target could start from (the first letter of the target)
    start_points = grid.match(target_word[0])

    # The number of occurrences (the answer)
    total = 0

    for start_point in start_points:                                # Try all the start points
        for direction in directions:                                # Try all directions from the start point
            word = []                                               # Keep track of the word we've got so far...
            viable = True                                           # ...and whether it's viable to continue in this direction...
            current_point = start_point                             # ...and how far along we've travelled
            while viable and len(word) < len(target_word):          # While the word we're forming in this direciton is valid
                word += grid.at(current_point)                      # Add the next letter to the word...
                current_point = current_point + direction           # ...and keep moving in this direction

                viable = (                                          # We can continue, so long as...
                    word_is_valid(word, target_word) and            # The word we've got so far is valid, and...
                    current_point.is_valid(grid)                    # ...we can go in the same direction without exceeding limits
                )

                if word == target_word:                             # If we've found our target...
                    total += 1                                      # ...increment our total

    return total


# How to count overlapping diagonal instances of a target word
def count_crossing_diagonals(grid: Grid, target_word: list) -> int:
    # Possible directions the target(s) could be oriented - diagonals only
    directions = [Point(-1, -1), Point(-1, 1)]

    # We're trying to find the centre of the 'X' - the middle char of the target word
    start_points = grid.match(target_word.pop(len(target_word) // 2))

    # The total number of occurrences (the answer)
    x_mas_total = 0

    for start_point in start_points:                                # Try all the start points
        subtot = 0                                                  # Keep track of how many lines crossing our start point are valid
        for direction in directions:                                # Try each of the lines (\ and /)

            up = start_point + direction                            # Get the diagonal start point 
            down = start_point + (direction * -1)                   # Get the diagonal end point

            if not(up.is_valid(grid) and down.is_valid(grid)):      # If either of those points aren't valid...
                break                                               # ...move on to another start point

            up_char = grid.at(up)                                   # Get the character from the diagonal start
            down_char = grid.at(down)                               # Get the character form the diagonal end

            if (                                                    # The diagonal is valid if...
                up_char in target_word and                          # The start of the diagonal is "M" or "S"; and
                down_char in target_word and                        # The end of the diagonal is "M" or "S"; and
                up_char != down_char                                # The start and end of the diagonal aren't the same
            ):
                subtot += 1                                         # Increment our subtotal if it's valid

        if subtot > 1:
            x_mas_total += 1                                        # Increment our grand total for each start point that is crossed twice

    return x_mas_total    


# Answers
grid = Grid("puzzle_4_input.txt")
print(count_words_in_grid(grid=grid, target_word=["X","M","A","S"]))
print(count_crossing_diagonals(grid=grid, target_word=["M","A","S"]))