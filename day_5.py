import pathlib
import pandas as pd
import numpy as np

def get_rules_and_sequences_from_file(input_file: str) -> tuple:
    with pathlib.Path(input_file).open("r") as in_file:
        lines = in_file.readlines()

    gap_index = lines.index("\n")

    rules = [
        [int(node) for node in line.strip("\n").split("|")]
        for line in lines[:gap_index]
    ]

    sequences = [
        [int(node) for node in line.strip("\n").split(",")]
        for line in lines[gap_index+1:]
    ]

    return (rules, sequences)

def get_node_matrix(rules: list) -> list:
    unique_nodes = set([node for rule in rules for node in rule])
    my_df = pd.DataFrame(index=list(unique_nodes), columns=list(unique_nodes))

    for rule in rules:
        big_node, little_node = rule
        my_df.loc[big_node, little_node] = 1
        my_df.loc[little_node, big_node] = -1

    return my_df

def get_node_order(node_matrix: pd.DataFrame, sequence: list) -> list:
    sub_matrix = node_matrix.loc[sequence][sequence]
    sub_matrix["total"] = sub_matrix.sum(axis=1)
    return sub_matrix["total"].sort_values(ascending=False).index.to_list()

def get_middle_page(sequence: list) -> int:
    return sequence[len(sequence) // 2]

def sequence_in_correct_order(sequence: list, correct_order: list) -> bool:
    index = [correct_order.index(item) for item in sequence]
    diffs = np.diff(index)
    direction = [diff > 0 for diff in diffs]
    return min(direction) == max(direction)


rules, sequences = get_rules_and_sequences_from_file("puzzle_5_input.txt")
node_matrix = get_node_matrix(rules)

total = 0

for sequence in sequences:
    node_order = get_node_order(node_matrix, sequence)
    if sequence_in_correct_order(sequence, node_order):
        total += get_middle_page(sequence)

print(total)

