import pdfplumber
import os
import pandas as pd

pdf_path = "Accenture_report.pdf"
pages_to_extract = [21, 27, 28, 29, 30, 31, 32, 33, 35, 37, 38, 39]

output_dir = "table_output"
os.makedirs(output_dir, exist_ok=True)

with pdfplumber.open(pdf_path) as pdf:
    table_count = 0
    for page_number in pages_to_extract:
        page = pdf.pages[page_number - 1]
        tables = page.extract_tables()

        for i, table in enumerate(tables):
            if table:
                df = pd.DataFrame(table)
                filename = f"page_{page_number}_table_{i+1}.csv"
                df.to_csv(os.path.join(output_dir, filename), index=False, header=False)
                print(f"Saved table from page {page_number} as {filename}")
                table_count += 1

print(f"Total tables extracted: {table_count}")
