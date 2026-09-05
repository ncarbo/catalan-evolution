from pathlib import Path
import re
import pandas as pd

METADATA_FILE = Path("metadata.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = Path("data/features_basic.csv")

df = pd.read_csv(METADATA_FILE)

rows = []

for _, row in df.iterrows():
    filename = row["filename"]
    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        print(f"Missing file: {filename}")
        continue

    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    words = re.findall(
        r"\b[\wÀ-ÿ·'-]+\b",
        text,
        flags=re.UNICODE
    )

    sentences = re.split(
        r"[.!?]+",
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    word_count = len(words)

    if word_count > 0:
        avg_word_length = (
            sum(len(word) for word in words)
            / word_count
        )
    else:
        avg_word_length = 0

    sentence_count = len(sentences)

    if sentence_count > 0:
        avg_sentence_length = (
            word_count
            / sentence_count
        )
    else:
        avg_sentence_length = 0

    unique_words = set(
        word.lower()
        for word in words
    )

    if word_count > 0:
        lexical_diversity = (
            len(unique_words)
            / word_count
        )
    else:
        lexical_diversity = 0

    punctuation_count = len(
        re.findall(
            r"[.,;:!?]",
            text
        )
    )

    if word_count > 0:
        punctuation_per_1000 = (
            punctuation_count
            / word_count
            * 1000
        )
    else:
        punctuation_per_1000 = 0

    rows.append({
        "id": row["id"],
        "filename": filename,
        "year": row["year"],
        "text_type": row["text_type"],
        "variant": row["variant"],
        "word_count": word_count,
        "avg_word_length": avg_word_length,
        "sentence_count": sentence_count,
        "avg_sentence_length": avg_sentence_length,
        "lexical_diversity": lexical_diversity,
        "punctuation_per_1000": punctuation_per_1000,
    })

features_df = pd.DataFrame(rows)

features_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print(f"Created {OUTPUT_FILE}")
print(f"Documents analyzed: {len(features_df)}")