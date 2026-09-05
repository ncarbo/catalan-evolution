from pathlib import Path
import re
import csv

INPUT_DIR = Path("data/external/external_processed")
OUTPUT_FILE = Path("data/metadata/external_metadata.csv")

WORD_RE = re.compile(r"\b[\wÀ-ÿ·'-]+\b", re.UNICODE)

rows = []

for path in INPUT_DIR.glob("*.txt"):
    text = path.read_text(encoding="utf-8", errors="ignore")

    source_match = re.search(r"<FONT>(.*?)</FONT>", text, re.DOTALL)
    title_match = re.search(r"<TÍTOL>(.*?)</TÍTOL>", text, re.DOTALL)
    year_match = re.search(r"<ANY>(.*?)</ANY>", text, re.DOTALL)
    type_match = re.search(r"<TIPUS_TEXT>(.*?)</TIPUS_TEXT>", text, re.DOTALL)
    variant_match = re.search(r"<VARIANT>(.*?)</VARIANT>", text, re.DOTALL)
    translation_match = re.search(r"<TRADUCCIO>(.*?)</TRADUCCIO>", text, re.DOTALL)
    ocr_match = re.search(r"<OCR>(.*?)</OCR>", text, re.DOTALL)
    body_match = re.search(r"<TEXT>(.*?)</TEXT>", text, re.DOTALL)

    body = body_match.group(1) if body_match else ""
    word_count = len(WORD_RE.findall(body))

    rows.append({
        "filename": path.name,
        "source": source_match.group(1) if source_match else "",
        "title": title_match.group(1) if title_match else "",
        "year": year_match.group(1) if year_match else "",
        "text_type": type_match.group(1) if type_match else "",
        "variant": variant_match.group(1) if variant_match else "",
        "translation": translation_match.group(1) if translation_match else "",
        "ocr": ocr_match.group(1) if ocr_match else "",
        "word_count": word_count,
    })

rows.sort(key=lambda x: (x["year"], x["source"], x["filename"]))

with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "filename",
            "source",
            "title",
            "year",
            "text_type",
            "variant",
            "translation",
            "ocr",
            "word_count",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Written: {OUTPUT_FILE}")
print(f"Documents: {len(rows)}")
print(f"Total words: {sum(r['word_count'] for r in rows):,}")