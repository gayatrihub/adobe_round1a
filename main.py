import fitz  # PyMuPDF
import os
import json
import re
from collections import defaultdict

def is_structured_pdf(texts):
    # Detect structure by matching lines like "1.", "2.1", etc.
    return sum(1 for t in texts if re.match(r"^\d+(\.\d+)*\s+", t)) >= 3

def extract_title_and_headings(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    headings = []

    font_info = defaultdict(list)  # {size: [(text, page_num)]}
    font_sizes = []
    all_texts = []

    for page_index, page in enumerate(doc):  # 0-based index here
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    text = span["text"].strip()
                    if len(text) < 2:
                        continue
                    font_info[size].append((text, page_index))
                    font_sizes.append(size)
                    all_texts.append(text)

    # Detect title: Largest font text (longer than 10 chars)
    max_size = max(font_info.keys())
    for text, _ in font_info[max_size]:
        if len(text) > 10:
            title = text
            break

    # Detect if structured or a form
    if not is_structured_pdf(all_texts):
        return {
            "title": title,
            "outline": []
        }

    # Sort sizes to assign levels
    unique_sizes = sorted(set(font_sizes), reverse=True)
    size_to_level = {}
    if len(unique_sizes) > 1:
        size_to_level[unique_sizes[1]] = "H1"
    if len(unique_sizes) > 2:
        size_to_level[unique_sizes[2]] = "H2"
    if len(unique_sizes) > 3:
        size_to_level[unique_sizes[3]] = "H3"

    # Collect headings
    for size, entries in font_info.items():
        level = size_to_level.get(size)
        if not level:
            continue
        for text, page_index in entries:
            if re.match(r"^\d+(\.\d+)*\s+", text) or level == "H1":
                headings.append({
                    "level": level,
                    "text": text,
                    "page": page_index  # ✅ 0-based page number
                })

    return {
        "title": title,
        "outline": headings
    }

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_output = extract_title_and_headings(pdf_path)

            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_dir, json_filename)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    process_all_pdfs("input", "output")
