import pandas as pd

df = pd.read_csv("output/capacity_clean.csv")

name_fixes = {
    "Chhatisgarh": "Chhattisgarh",
    "Lakshwadeep": "Lakshadweep",
    "Dadar & Nagar Have": "Dadra & Nagar Haveli and Daman & Diu",
    "Dadar & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu",
    "Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
    "Dadar & Nagar Haveli/ Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu",
}
df["state"] = df["state"].replace(name_fixes)

# Where a state now appears twice in a year (Dadra + Daman), add the rows together
number_cols = ["small_hydro_mw", "wind_mw", "bio_power_mw", "solar_mw", "total_mw"]
df = df.groupby(["year", "state"], as_index=False)[number_cols].sum()
df = df.sort_values(["year", "state"]).reset_index(drop=True)

df[number_cols] = df[number_cols].round(2)
df.to_csv("output/capacity_final.csv", index=False)

print("Saved output/capacity_final.csv")
print("Total rows:", len(df))
print("Unique states:", df["state"].nunique())
print()
print("Year | States | Total MW")
print(df.groupby("year").agg(states=("state", "count"), total=("total_mw", "sum")).round(2).to_string())