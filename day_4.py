import itertools

from grid import Grid, Point
        

def count_words_in_grid(grid: Grid, target_word: list) -> int:
    """Count the occurrences of the target word in the input grid."""
    directions = [                                                  # Possible directions the target could be oriented 
        Point(*move)
        for move in itertools.product([-1, 0, 1], repeat=2) 
        if move != (0, 0)
    ]

    start_points = grid.match(target_word[0])                       # The places the target could start from (the first letter of the target)

    total = 0                                                       # The number of occurrences (the answer)

    for start_point in start_points:                                # Try all the start points
        for direction in directions:                                # Try all directions from the start point  

            final_point = (                                         # Get the point at the end of the word in this direction
                start_point + 
                (direction * (len(target_word) -1))
            )

            if not final_point.is_valid(grid):                      # If that point is 'off-grid'...
                continue                                            # ...don't continue with this direction

            current_point = start_point                             
            word = [grid.at(current_point)]

            while (                                                 
                word == target_word[:len(word)] and                 # While the word we have is still correct...
                len(word) < len(target_word)                        # ...and we've not found the full word
            ):
                current_point += direction                          # Keep moving in this direction...
                word += grid.at(current_point)                      # ...adding a letter to the word as we go

                if word == target_word:
                    total += 1
    return total


def count_crossing_diagonals(grid: Grid, target_word: list) -> int:
    """Count times a target word overlaps in an 'X' pattern in an input grid."""
    directions = [Point(-1, -1), Point(-1, 1)]                      # Possible directions the target(s) could be oriented - diagonals only

    start_points = [                                                # We're trying to find the centre of the 'X'...
        point
        for point in grid.match(
            target_word.pop(len(target_word) // 2)                  # ...the middle char of the target word...
        )
        if not point.is_on_boundary(grid)                           # ...but only if that char is not on the edge of the grid
    ]

    total = 0                                                       # The total number of occurrences (the answer)

    for start_point in start_points:                                # Try all the start points
        subtot = 0                                                  # Keep track of how many lines crossing our start point are valid
        for direction in directions:                                # Try each of the lines (\ and /)

            up_char = grid.at(start_point + direction)              # Get the character from the diagonal start
            down_char = grid.at(start_point + (direction * -1))     # Get the character form the diagonal end

            if (                                                    # The diagonal is valid if...
                up_char in target_word and                          # ...the start of the diagonal is in the target word; and...
                down_char in target_word and                        # ...the end of the diagonal is in the target word, and..
                up_char != down_char                                # ...the start and end of the diagonal aren't the same
            ):
                subtot += 1                                         # Increment our subtotal if it's valid

        if subtot > 1:
            total += 1                                              # Increment our grand total for each start point that is crossed twice

    return total    

# Answers
grid = Grid("puzzle_4_input.txt")
print(count_words_in_grid(grid=grid, target_word=["X","M","A","S"]))
print(count_crossing_diagonals(grid=grid, target_word=["M","A","S"]))
