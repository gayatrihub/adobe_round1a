# 🧠 Adobe Hackathon Round 1A — Structured PDF Outline Extractor

## 📘 Challenge Summary

Extract a clean, structured outline (Title, H1, H2, H3) from **any PDF document** — and output it as a valid JSON. This outline powers intelligent navigation, summarization, and downstream document understanding systems.

---

## 🎯 Problem We Solved

PDFs can be:
- 📄 Well-structured reports (with numbered headings)
- 🧾 Forms (like government templates, invoices, etc.)
- 📚 Text-heavy scanned documents

**Naive solutions fail** when forms or templates contain field labels like `"1. Name"`, which resemble headings.  
We addressed this head-on.

---

## 💡 Our Approach

### 🧪 Input: `/input/file01.pdf`
A flat government form with field labels like:
```
1. Name of the Government Servant
2. Designation
...
```

> Most extractors would wrongly treat these as H1/H2 headings!

---

### ✅ Output: `/output/file01.json`

```json
{
  "title": "Application form for grant of LTC advance",
  "outline": []
}
```

✔️ **Correctly detects only the title**  
✔️ **No false heading extraction**  
✔️ **Exactly matches the expected JSON format**

---

## 🧬 Solution Architecture

```mermaid
flowchart TD
    A[PDF Input] --> B[Text Extraction (PyMuPDF)]
    B --> C[Font Size Ranking]
    C --> D[Regex Filter for Heading Structure]
    D --> E{Structured Document?}
    E -- Yes --> F[Extract H1/H2/H3 with page number]
    E -- No --> G[Return only title]
    F & G --> H[JSON Output]
```

---

## 🛠️ Implementation Highlights

| Feature                     | Why It Matters                                            |
|-----------------------------|-----------------------------------------------------------|
| 🎯 Title Detection          | Based on largest font text on first page                  |
| 🧩 Heading Classification   | Uses relative font size and numbering patterns            |
| 🧾 Form Detection Logic     | Skips headings if the doc looks like a flat form          |
| 🧠 Regex Rules              | Matches true structural patterns like `1.`, `2.1`, etc.   |
| 🧼 Clean Output             | No garbage headings, strictly valid JSON                  |

---

## 🔍 How to Run

```bash

docker build --platform=linux/amd64 -t adobe-document-extractor .

docker run --platform=linux/amd64 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  adobe-document-extractor
```


Ensure the folder structure:
```
project/
├── input/
│   └── file01.pdf
├── output/
├── main.py
```

---

## 🧪 Sample Output Evaluation

| File        | Title                                | Headings Extracted | JSON Valid |
|-------------|----------------------------------------|--------------------|-------------|
| file01.pdf  | ✅ Application form for LTC advance   | ✅ None (expected) | ✅ Yes       |

---

## 🤝 Why Our Solution Stands Out

| Others May...                             | Our Solution Does...                                      |
|-------------------------------------------|------------------------------------------------------------|
| ❌ Extract all numbered lines as headings | ✅ Checks if doc is structured first                      |
| ❌ Rely only on font size                 | ✅ Combines font + numbering + structure detection        |
| ❌ Fail on flat forms                     | ✅ Skips heading extraction when no clear structure exists |
| ❌ Hardcode for one format                | ✅ Works across templates and languages (extensible)      |

---

## 📦 Tech Stack

- Python 3.10
- PyMuPDF (`fitz`)
- Regex, font clustering
- Fully offline & Docker-ready

---

## 🧠 Future Enhancements

- Add multilingual heading detection (e.g., Japanese)
- Optional ML-based validator under 200MB
- Integrate into a smart reader for Round 1B

---

## 🙌 Conclusion

This isn’t just about extracting headings — it’s about **understanding the intent of the document**.  
Our extractor respects structure, skips noise, and adapts smartly.

> “Not everything numbered is a heading. Our solution gets that.”

---