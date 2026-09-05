from pathlib import Path
import re

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

processed_count = 0
failed_files = []

for file_path in RAW_DIR.glob("*.txt"):
    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    body_match = re.search(
        r"<TEXT>(.*?)</TEXT>",
        text,
        re.S
    )

    if not body_match:
        failed_files.append(file_path.name)
        continue

    body = body_match.group(1)

    # Normalize line endings
    body = body.replace("\r\n", "\n")
    body = body.replace("\r", "\n")

    # Remove spaces/tabs before line breaks
    body = re.sub(
        r"[ \t]+\n",
        "\n",
        body
    )

    # Collapse multiple spaces/tabs inside lines
    body = re.sub(
        r"[ \t]{2,}",
        " ",
        body
    )

    # Avoid huge blocks of empty lines
    body = re.sub(
        r"\n{3,}",
        "\n\n",
        body
    )

    body = body.strip()

    output_path = PROCESSED_DIR / file_path.name

    output_path.write_text(
        body,
        encoding="utf-8"
    )

    processed_count += 1

print(f"Processed files: {processed_count}")
print(f"Failed files: {len(failed_files)}")

if failed_files:
    print("\nFiles without <TEXT>...</TEXT>:")
    for filename in failed_files:
        print(filename)