import re
import pathlib
from operator import mul
from functools import reduce

# Get the input
with pathlib.Path("puzzle_3_input.txt").open("r") as in_file:
    in_text = in_file.read()

# ---- Day 3, PT 1---- #

# Find the valid instructions
instructions = re.findall(r'mul\([0-9]*,[0-9]*\)', in_text)

# Convert the instructions to lists of numbers
def format_instructions(instructions: list) -> list:
    return [
        [int(num) for num in instruction[4:-1].split(",")]
        for instruction in instructions
    ]

instructions = format_instructions(instructions)

# Reduce the lists to find the answer
answer = sum([reduce(mul, instruction) for instruction in instructions])
print(answer)


# ---- Day 3, PT 2---- #

# Find all valid instructions - including conditions
instructions_including_conditions = re.findall(
    r'mul\([0-9]*,[0-9]*\)|don\'t\(\)|do\(\)', in_text
)

# Filter the instructions based on do/dont'
def filter_instructions(instructions: list) -> list:
    filtered_instructions = []
    include_flag = True
    for instruction in instructions:

        if instruction == "don't()":
            include_flag = False
            continue

        if instruction == "do()":
            include_flag = True
            continue

        if include_flag:
            filtered_instructions.append(instruction)

    return filtered_instructions

# Filter and format the instructions
filtered_instructions = filter_instructions(instructions_including_conditions)
formatted_instructions = format_instructions(filtered_instructions)

# Get the answer
answer_2 = sum([reduce(mul, instruction) for instruction in formatted_instructions])
print(answer_2)
