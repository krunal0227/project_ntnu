from pdf2image import convert_from_path
from PIL import Image
import os

# --- Step 1: PDF and Poppler Paths ---
pdf_path = "Accenture_report.pdf"
poppler_path = r"C:\poppler\bin"  # <-- Update this to your actual path
output_dir = "pdf_preview"
os.makedirs(output_dir, exist_ok=True)

# --- Step 2: Convert PDF Pages to Images ---
pages = convert_from_path(pdf_path, dpi=150, poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')

# --- Step 3: Save each page as a preview image ---
for i, page in enumerate(pages):
    # Resize for thumbnail preview (optional)
    preview = page.copy()
    preview.thumbnail((800, 1000))  # Resize while keeping aspect ratio

    filename = f"preview_page_{i + 1}.png"
    image_path = os.path.join(output_dir, filename)
    preview.save(image_path, "PNG")
    print(f"Preview saved: {filename}")

print(f"\n {len(pages)} page previews saved to '{output_dir}'")
