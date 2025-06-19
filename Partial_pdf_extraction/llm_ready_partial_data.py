import os
import re
import json
import pandas as pd
from nltk.tokenize import sent_tokenize

# Root folder containing all parts
base_dir = "Partial_pdf_extraction"

# Subdirectories
text_dir = os.path.join(base_dir, "part_text_output")
image_dir = os.path.join(base_dir, "part_image_output")
table_dir = os.path.join(base_dir, "part_table_output")

# Output file
output_path = os.path.join(base_dir, "llm_dataset.jsonl")

# Storage
dataset = []

# --- Process Text Files ---
print("Processing text files...")
for file in sorted(os.listdir(text_dir)):
    if file.endswith(".txt"):
        page_number = re.findall(r'\d+', file)[0]
        with open(os.path.join(text_dir, file), "r", encoding="utf-8") as f:
            text = f.read()
            sentences = sent_tokenize(re.sub(r'\s+', ' ', text.strip()))
            for sentence in sentences:
                dataset.append({
                    "page": int(page_number),
                    "type": "text",
                    "content": sentence.strip()
                })

# --- Process Table Files ---
print("Processing table CSVs...")
for file in sorted(os.listdir(table_dir)):
    if file.endswith(".csv"):
        match = re.search(r'page_(\d+)', file)
        page_number = match.group(1) if match else "unknown"
        dataset.append({
            "page": int(page_number),
            "type": "table",
            "content": f"[Table saved at: part_table_output/{file}]"
        })

# --- Process Image Files ---
print("Processing images...")
for file in sorted(os.listdir(image_dir)):
    if re.match(r'page_\d+_img_\d+\.(png|jpg|jpeg)', file, re.IGNORECASE):
        page_number = re.findall(r'\d+', file)[0]
        dataset.append({
            "page": int(page_number),
            "type": "image",
            "content": f"[Image saved at: part_image_output/{file}]"
        })

# --- Save to JSONL ---
print(f"Saving dataset to {output_path} ...")
with open(output_path, "w", encoding="utf-8") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

print(f"LLM-ready dataset created: {output_path}")
print(f"Total entries: {len(dataset)}")
