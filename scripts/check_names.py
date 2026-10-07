import pandas as pd

df = pd.read_csv("output/capacity_clean.csv")
total_years = df["year"].nunique()

# For each state name, list the years it appears in
years_by_state = df.groupby("state")["year"].apply(lambda s: sorted(s.tolist()))

print("State names that do NOT appear in all", total_years, "years:")
print("-" * 60)
for state, years in years_by_state.items():
    if len(years) < total_years:
        print(f"{state}: {years}")

print()
print("All unique state names:", len(years_by_state))
