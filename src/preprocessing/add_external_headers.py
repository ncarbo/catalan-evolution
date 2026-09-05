from pathlib import Path
import re

INPUT_DIR = Path("data/external/external_processed")

def get_metadata(filename: str):
    name = filename.lower()

    year_match = re.search(r"(19\d{2})", name)
    year = year_match.group(1) if year_match else "unknown"

    if name.startswith("ariel"):
        source = "Ariel"
    elif name.startswith("res_") or name.startswith("ressorgiment"):
        source = "Ressorgiment"
    else:
        source = "unknown"

    return source, year


for path in INPUT_DIR.glob("*.txt"):
    text = path.read_text(encoding="utf-8", errors="ignore")

    if text.lstrip().startswith("<DOCUMENT"):
        print(f"SKIP: {path.name} already has startblock")
        continue

    source, year = get_metadata(path.name)

    title = path.stem.replace("_", " ")

    header = f"""<DOCUMENT source="external">
<OBRA>
<FONT>{source}</FONT>
<TÍTOL>{title}</TÍTOL>
<ANY>{year}</ANY>
<TIPUS_TEXT>MIXED</TIPUS_TEXT>
<VARIANT>unknown</VARIANT>
<TRADUCCIO>mixed</TRADUCCIO>
<OCR>yes</OCR>
</OBRA>
<TEXT>
"""

    footer = """
</TEXT>
</DOCUMENT>
"""

    new_text = header + text.strip() + footer

    path.write_text(new_text, encoding="utf-8")

    print(f"OK: {path.name} -> {source}, {year}")