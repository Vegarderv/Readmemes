import pandas as pd
import numpy as np
import json
from datetime import datetime

start_month = 4
start_year = 2016

months = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]

messages = pd.read_json("messages2.json")

with open("users.json", "r", encoding="utf8") as f:
    userplot = json.loads(f.read())
userplot[np.nan] = "NaN"

messages["month"] = messages["ts"].apply(lambda x: datetime.utcfromtimestamp(x).month)
messages["year"] = messages["ts"].apply(lambda x: datetime.utcfromtimestamp(x).year)

messages = messages.sort_values(by=['year', 'month'])

print(messages.iloc[999])


def get_index(year, month):
    return (year - start_year) * 12 + month - start_month

# Create Matrix
names = userplot.keys()

matrix = {name : [0]* (12 * 6 + 11 + 9) for name in names}

for index, row in messages.iterrows():
    matrix[row["user"]][get_index(row["year"], row["month"])] += 1

for name in names:
    total = 0
    total_list = matrix[name]
    for i in range(len(total_list)):
        total += total_list[i]
        total_list[i] = total

months_year = {"name" : []}
curr_month = start_month
curr_year = start_year

while curr_month != 12 or curr_year != 2023:
    months_year[f"{months[curr_month - 1]}, {curr_year}"] = []
    curr_month += 1
    if curr_month == 13:
        curr_month = 1
        curr_year += 1

final_df = pd.DataFrame(months_year)

for name in names:
    final_df.loc[len(final_df.index)] = [userplot[name]] + matrix[name]

final_df.to_csv("race.csv")
