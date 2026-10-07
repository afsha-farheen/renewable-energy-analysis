import sqlite3
import pandas as pd

df = pd.read_csv("output/capacity_final.csv")

conn = sqlite3.connect("output/renewable_energy.db")

# Create (or replace) the table from the CSV data
df.to_sql("state_capacity", conn, if_exists="replace", index=False)

print("Database built: output/renewable_energy.db")
print("Rows saved:", len(df))
print()

# Test query 1: India's total capacity by year
print("1) Total capacity by year (MW):")
q1 = """
SELECT year, ROUND(SUM(total_mw), 0) AS total_mw
FROM state_capacity
GROUP BY year
ORDER BY year
"""
print(pd.read_sql(q1, conn).to_string(index=False))

# Test query 2: Top 5 states in 2024
print()
print("2) Top 5 states in 2024:")
q2 = """
SELECT state, total_mw
FROM state_capacity
WHERE year = 2024
ORDER BY total_mw DESC
LIMIT 5
"""
print(pd.read_sql(q2, conn).to_string(index=False))

# Test query 3: Growth of solar vs wind, 2015 vs 2024
print()
print("3) Solar and wind in India, 2015 vs 2024 (MW):")
q3 = """
SELECT year, ROUND(SUM(solar_mw), 0) AS solar_mw, ROUND(SUM(wind_mw), 0) AS wind_mw
FROM state_capacity
WHERE year IN (2015, 2024)
GROUP BY year
ORDER BY year
"""
print(pd.read_sql(q3, conn).to_string(index=False))

conn.close()