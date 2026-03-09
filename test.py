import json
import pandas as pd

with open("result_attack.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

expanded_df = df["filtered_papers"].apply(pd.Series)

# Save the "site" column to a txt file
expanded_df["site"].to_csv(
    "site.txt",
    index=False,
    header=False
)
