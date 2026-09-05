from pathlib import Path
import re

INPUT_DIR = Path("data/external/external_txt")
OUTPUT_DIR = Path("data/external/external_processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

processed = 0

for path in INPUT_DIR.glob("*.txt"):
    text = path.read_text(encoding="utf-8", errors="ignore")

    #normalizes page jumps and line jumps
    text = text.replace("\f", "\n")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    #unites words divided by - (end of line)
    #ex: "lite-\nratura" -> "literatura"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    #eliminates page numbers
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)

    #eliminates extra spaces at end of line
    text = re.sub(r"[ \t]+\n", "\n", text)

    #collapses multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    #collapses line
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip()

    out = OUTPUT_DIR / path.name
    out.write_text(text, encoding="utf-8")

    processed += 1
    print(f"OK: {path.name}")

print(f"\nProcessed external files: {processed}")