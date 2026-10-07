import pdfplumber
from pathlib import Path

reports = Path("reports")

for pdf_path in sorted(reports.glob("RE_Capacity_*.pdf")):
    print("=" * 60)
    print(pdf_path.name)
    with pdfplumber.open(pdf_path) as pdf:
        print("Pages:", len(pdf.pages))
        page = pdf.pages[0]
        text = page.extract_text() or ""
        lines = text.split("\n")
        print("First 12 lines of page 1:")
        for line in lines[:12]:
            print("   ", line)
        tables = page.extract_tables()
        print("Tables found on page 1:", len(tables))