import collections
import pathlib
import operator
import itertools

operators = ("+", "*", "||")

with pathlib.Path("puzzle_input_7.txt").open("r") as in_file:
    problems = {
        int(line.split(":")[0]):
        [
            int(number)
            for number in line.split(":")[1].strip("\n").lstrip().split(" ")
        ]
        for line in in_file
    }

def valid_op(target: int, inputs: list, operators:tuple=operators) -> bool:
    for combo in itertools.product(operators, repeat=len(inputs)-1):
        my_combo = list(combo)
        my_inputs = inputs[:]

        subtotal = my_inputs.pop(0)

        for index, op in enumerate(my_combo):
            if op == "+":
                subtotal += my_inputs.pop(0)

            if op == "*":
                subtotal *= my_inputs.pop(0)

            if op == "||":
                subtotal = int(str(subtotal) + str(my_inputs.pop(0)))

        if subtotal == target:
            return True
    return False
    

answer = sum(
    target 
    for target, inputs in problems.items() 
    if valid_op(target, inputs, operators[:2])
)

answer_pt_2 = sum(
    target
    for target, inputs in problems.items()
    if valid_op(target, inputs, operators)
)

print(answer_pt_2)



