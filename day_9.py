import pathlib
import textwrap
import time
import re

with pathlib.Path("puzzle_input_9_3.txt").open("r") as in_file:
    full_map_str = in_file.read()


def odds_and_evens(string: str) -> tuple:
    evens = []
    odds = []

    for index, char in enumerate(full_map_str):
        if index % 2 == 0:
            evens.append(full_map_str[index])
        else:
            odds.append(full_map_str[index])
    
    print(odds, evens)
    return (odds, evens)


def get_disk_map(string: str) -> list:
    output = []
    for index, block in enumerate(textwrap.wrap(string, 2)):
        output += [index] * int(block[0])
        if len(block) > 1:
            output += [-1] * int(block[1])

    return output


def defrag_2(disk_map: list, odds: list, evens: list) -> list:
    pass


def defrag(disk_map: list) -> list:
    """Defrag"""
    # Get indexes of the spaces in the first half
    print(disk_map)
    no_spaces = []
    space_indexes = []

    for index, item in enumerate(disk_map):
        if item != -1:
            no_spaces.append(item)
        else:
            space_indexes.append(index)

    for index in space_indexes:
        no_spaces.insert(index, no_spaces.pop())

    no_spaces += [-1] * (len(disk_map) - len(no_spaces))
    return no_spaces


def checksum(disk_map: str) -> int:
    """Checksum"""
    checksum = sum(
        num * index for 
        index, num in enumerate(disk_map) 
        if num != -1
    )
    return checksum


disk_map = get_disk_map(full_map_str)
defrag_result = defrag(disk_map)
checksum_result = checksum(defrag_result)

defrag_2_result = defrag_2(disk_map, *odds_and_evens(full_map_str))