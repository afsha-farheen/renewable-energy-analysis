import re
import pdfplumber
import pandas as pd
from pathlib import Path

reports = Path("reports")
Path("output").mkdir(exist_ok=True)


def to_number(value):
    """Turn a table cell into a number. Blank cells become 0.0."""
    if value is None:
        return 0.0
    text = str(value).replace(",", "").strip()
    if text in ("", "-", "--", "None"):
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def clean_name(value):
    """Remove line breaks and extra spaces from a state name."""
    return re.sub(r"\s+", " ", str(value)).strip()


all_rows = []

print("Year | States | Sum of states | Reported total | Difference")
print("-" * 60)

for pdf_path in sorted(reports.glob("RE_Capacity_*.pdf")):
    year = int(re.search(r"(\d{4})", pdf_path.stem).group(1))

    with pdfplumber.open(pdf_path) as pdf:
        tables = pdf.pages[0].extract_tables()
    table = max(tables, key=len)

    year_rows = []
    reported_total = 0.0

    for row in table:
        if len(row) < 11:
            continue
        first = (row[0] or "").strip()
        second = clean_name(row[1]) if row[1] else ""

        if first.isdigit() and second:
            year_rows.append({
                "year": year,
                "state": second,
                "small_hydro_mw": to_number(row[2]),
                "wind_mw": to_number(row[3]),
                "bio_power_mw": to_number(row[8]),
                "solar_mw": to_number(row[-2]),
                "total_mw": to_number(row[-1]),
            })
        elif second.startswith("Total"):
            reported_total = to_number(row[-1])

    our_sum = sum(r["total_mw"] for r in year_rows)
    diff = round(our_sum - reported_total, 2)
    print(f"{year} | {len(year_rows):>6} | {our_sum:>13.2f} | {reported_total:>14.2f} | {diff}")

    all_rows.extend(year_rows)

df = pd.DataFrame(all_rows)
df.to_csv("output/capacity_clean.csv", index=False)

print()
print("Saved output/capacity_clean.csv")
print("Total rows:", len(df))
print(df.head(5).to_string(index=False))