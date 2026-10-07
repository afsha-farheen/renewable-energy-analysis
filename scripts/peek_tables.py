import pdfplumber
from pathlib import Path

reports = Path("reports")

for pdf_path in sorted(reports.glob("RE_Capacity_*.pdf")):
    print("=" * 60)
    print(pdf_path.name)
    with pdfplumber.open(pdf_path) as pdf:
        tables = pdf.pages[0].extract_tables()
        if not tables:
            print("No table found")
            continue
        table = max(tables, key=len)
        print("Rows:", len(table), "| Columns:", len(table[0]))
        print("First 6 rows:")
        for row in table[:6]:
            print("   ", [str(c).replace("\n", " ") for c in row])
        print("Last 2 rows:")
        for row in table[-2:]:
            print("   ", [str(c).replace("\n", " ") for c in row])