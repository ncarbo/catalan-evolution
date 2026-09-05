from pathlib import Path
import re
import csv

RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/metadata/metadata.csv")
rows = []

for file_path in RAW_DIR.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8", errors="ignore")

    obra_id = re.search(r'<OBRA id="([^"]+)">', text)
    autor = re.search(r'<AUTOR>(.*?)</AUTOR>', text, re.S)
    titol = re.search(r'<TÍTOL>(.*?)</TÍTOL>', text, re.S)
    any_ = re.search(r'<ANY>(.*?)</ANY>', text)
    body_match = re.search(
        r"<TEXT>(.*?)</TEXT>",
        text,
        re.S
    )

    if body_match:
        body = body_match.group(1)

        words = re.findall(
            r"\b[\wÀ-ÿ·'-]+\b",
            body,
            flags=re.UNICODE
        )

        word_count = len(words)
    else:
        word_count = None

    classificacio = re.search(
        r'<CLASSIFICACIÓ_TEXTUAL\s+llengua="([^"]*)"\s+gènere="([^"]*)"\s+tema="([^"]*)"\s+subtema="([^"]*)"\s+traducció="([^"]*)"\s+variant="([^"]*)"',
        text
    )

    row = {
        "id": obra_id.group(1) if obra_id else "",
        "filename": file_path.name,
        "author": autor.group(1).strip() if autor else "",
        "title": titol.group(1).strip() if titol else "",
        "year": any_.group(1).strip() if any_ else "",
        "text_type": classificacio.group(1) if classificacio else "",
        "genre": classificacio.group(2) if classificacio else "",
        "translation": classificacio.group(5) if classificacio else "",
        "variant": classificacio.group(6) if classificacio else "",
        "word_count": word_count,
    }

    rows.append(row)

with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "filename",
            "author",
            "title",
            "year",
            "text_type",
            "genre",
            "translation",
            "variant",
            "word_count",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)

print(f"Created {OUTPUT_FILE} with {len(rows)} documents. \n")