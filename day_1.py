import pathlib
import pandas as pd
import numpy as np
import time
import json

# ---- Day 1, PT 1 ---- #

# The Dataframe
df = pd.read_csv("puzzle_1_input.txt", sep="\\s+", names=["left", "right"])

# Sort the left hand side in place
df["left"] = df["left"].sort_values(ascending=True).values

# Sort the right hand side in place
df["right"] = df["right"].sort_values(ascending=True).values

# Get the difference between RHS/LHS items
df["diff"] = df["left"] - df["right"]

# ANSWER
answer_1 = df["diff"].abs().sum()
print(answer_1)


# ---- Day 1, PT 2 ---- #

# The number of occurrences of values on the right
value_counts = df["right"].value_counts()

# Merge those back in based on left/right comparison
df = pd.merge(df, value_counts, "left", left_on="left", right_index=True)

# Calculate similarity (left * number of occurrences)
df["similarity"] = df["left"] * df["count"]

# ANSWER
answer_2 = df["similarity"].sum()
print(answer_2)





    








