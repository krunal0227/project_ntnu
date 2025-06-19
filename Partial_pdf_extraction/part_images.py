import fitz  # PyMuPDF
from PIL import Image
import io
import os

pdf_path = "Accenture_report.pdf"
pages_to_extract = [21, 27, 28, 29, 30, 31, 32, 33, 35, 37, 38, 39]

output_dir = "image_output"
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
image_count = 0

for page_num in pages_to_extract:
    page = doc[page_num - 1]
    images = page.get_images(full=True)

    for img_index, img in enumerate(images, start=1):
        try:
            base_image = doc.extract_image(img[0])
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))

            filename = f"page_{page_num}_img_{img_index}.{image_ext}"
            image.save(os.path.join(output_dir, filename))
            print(f"Saved image from page {page_num}: {filename}")
            image_count += 1
        except Exception as e:
            print(f"Failed to extract image from page {page_num}: {e}")

doc.close()
print(f"Total images extracted: {image_count}")
