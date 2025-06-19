import re
from pdfminer.high_level import extract_text

# Path to the uploaded PDF file
pdf_path = "Accenture_report.pdf"

# Extract the full text from the PDF
full_text = extract_text(pdf_path)

# Save the extracted text to a file (optional)
with open("Accenture_report_extracted.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

# Example: Use regex to extract specific financial metrics (optional)
# Extract Revenue, Free Cash Flow, EPS, etc.
revenue_match = re.search(r"Revenues\s+\$([\d\.]+)B", full_text)
free_cash_flow_match = re.search(r"Free cash flow\s+\$([\d\.]+)B", full_text)
eps_match = re.search(r"Diluted earnings per share \(Adjusted\)\s+\$([\d\.]+)", full_text)

# Print extracted values
if revenue_match:
    print("Revenue:", revenue_match.group(1), "Billion USD")
if free_cash_flow_match:
    print("Free Cash Flow:", free_cash_flow_match.group(1), "Billion USD")
if eps_match:
    print("Adjusted EPS:", eps_match.group(1))

# If needed, search for any other patterns with re.findall or re.search
# For example, all monetary values:
all_money_values = re.findall(r"\$[\d\.]+B", full_text)
print("\nAll Billion-dollar Figures Found:")
print(all_money_values)
