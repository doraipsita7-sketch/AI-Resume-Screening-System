
# import os
# print(os.listdir("dataset/archive (2)/Resume"))

import pandas as pd

df = pd.read_csv("dataset/archive (2)/Resume/Resume.csv")

print(df["Category"].value_counts())
print("\nUnique Categories:\n")
print(df["Category"].unique())