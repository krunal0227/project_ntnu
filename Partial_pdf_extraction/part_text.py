from pdfminer.high_level import extract_text
import os

pdf_path = "Accenture_report.pdf"
pages_to_extract = [21, 27, 28, 29, 30, 31, 32, 33, 35, 37, 38, 39]

output_dir = "text_output"
os.makedirs(output_dir, exist_ok=True)

for page_number in pages_to_extract:
    # pdfminer is 0-indexed internally
    text = extract_text(pdf_path, page_numbers=[page_number - 1])
    file_path = os.path.join(output_dir, f"page_{page_number}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted text from page {page_number}")
