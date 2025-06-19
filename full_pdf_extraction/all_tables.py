import pdfplumber
import os
import pandas as pd

pdf_path = "Accenture_report.pdf"
output_dir = "extracted_tables"
os.makedirs(output_dir, exist_ok=True)

with pdfplumber.open(pdf_path) as pdf:
    table_count = 0
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()

        for j, table in enumerate(tables):
            if table:
                df = pd.DataFrame(table)
                filename = f"page_{i+1}_table_{j+1}.csv"
                csv_path = os.path.join(output_dir, filename)
                df.to_csv(csv_path, index=False, header=False)
                print(f"Extracted: {filename}")
                table_count += 1

print(f"\nTotal tables extracted: {table_count}")
