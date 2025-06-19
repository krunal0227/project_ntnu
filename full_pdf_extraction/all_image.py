import fitz  # PyMuPDF
from PIL import Image
import io
import os

# --- Step 1: Setup paths ---
pdf_path = "Accenture_report.pdf"
output_dir = "extracted_images"
os.makedirs(output_dir, exist_ok=True)

# --- Step 2: Open PDF ---
doc = fitz.open(pdf_path)
image_count = 0

# --- Step 3: Loop through pages and extract images ---
for page_number in range(len(doc)):
    page = doc[page_number]
    image_list = page.get_images(full=True)

    if not image_list:
        continue

    for img_index, img in enumerate(image_list, start=1):
        xref = img[0]
        try:
            # Extract image bytes
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            # Construct output path
            filename = f"page_{page_number + 1}_img_{img_index}.{image_ext}"
            image_path = os.path.join(output_dir, filename)

            # Save the image
            image.save(image_path)
            print(f"Extracted: {filename}")
            image_count += 1
        except Exception as e:
            print(f"Error extracting image on page {page_number + 1}: {e}")

doc.close()
print(f"\n Total images extracted: {image_count}")
