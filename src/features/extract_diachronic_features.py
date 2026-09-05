from pathlib import Path
import re
import csv
import pandas as pd

CTILC_DIR = Path("data/processed")
EXTERNAL_DIR = Path("data/external/external_processed")

CTILC_METADATA = Path("data/metadata/metadata.csv")
EXTERNAL_METADATA = Path("data/metadata/external_metadata.csv")

OUTPUT_FILE = Path("data/features/features_diachronic.csv")

WORD_RE = re.compile(
    r"\b[\wÀ-ÿ·'-]+\b",
    re.UNICODE,
)


PATTERNS = {
    # Historical alternatives
    "y": r"\by\b",
    "i": r"\bi\b",

    "ab": r"\bab\b",
    "amb": r"\bamb\b",

    "lo": r"\blo\b",
    "los": r"\blos\b",
    "el": r"\bel\b",
    "els": r"\bels\b",

    # Accents
    "a_acute": r"á",
    "a_grave": r"à",

    # Orthographic sequences
    "cedilla": r"ç",
    "ny": r"ny",
    "ss": r"ss",
    "qu_diaeresis": r"qü",
}

def count_plural_as(words):
    return sum(
        1
        for word in words
        if len(word) >= 2
        and word.lower().endswith("as")
    )

def count_plural_es(words):
    return sum(
        1
        for word in words
        if len(word) >= 2
        and word.lower().endswith("es")
    )

def count_h_letters(text):
    return len(
        re.findall(
            r"h",
            text,
            flags=re.IGNORECASE,
        )
    )

def count_final_ch(words):
    return sum(
        1
        for word in words
        if word.lower().endswith("ch")
    )

def count_final_c(words):
    return sum(
        1
        for word in words
        if word.lower().endswith("c")
    )

def extract_text(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<TEXT>(.*?)</TEXT>", text, re.DOTALL)

    return match.group(1) if match else text


def count_pattern(text, pattern):
    return len(
        re.findall(pattern, text, flags=re.IGNORECASE | re.UNICODE,)
    )


def normalize_count(count, word_count):
    if word_count == 0:
        return 0.0
    return count / word_count * 10_000


def extract_features(text):
    words = WORD_RE.findall(text)
    word_count = len(words)

    features = {"word_count": word_count}

    # Regex-based features
    for feature, pattern in PATTERNS.items():

        count = count_pattern(text, pattern)

        features[f"{feature}_count"] = count
        features[f"{feature}_freq_10k"] = normalize_count(count, word_count)

    # Token-based features
    plural_as_count = count_plural_as(words)
    features["plural_as_count"] = plural_as_count
    features["plural_as_freq_10k"] = normalize_count(plural_as_count, word_count)

    plural_es_count = count_plural_es(words)
    features["plural_es_count"] = plural_es_count
    features["plural_es_freq_10k"] = normalize_count(plural_es_count, word_count)

    h_count = count_h_letters(text)
    features["h_count"] = h_count 
    features["h_freq_10k"] = normalize_count(h_count, word_count)

    final_ch_count = count_final_ch(words)
    features["final_ch_count"] = final_ch_count
    features["final_ch_freq_10k"] = normalize_count(final_ch_count, word_count)

    final_c_count = count_final_c(words)
    features["final_c_count"] = final_c_count
    features["final_c_freq_10k"] = normalize_count(final_c_count, word_count)

    return features


def process_document(meta, data_dir, default_source=None):
    path = data_dir / meta["filename"]

    if not path.exists():
        print(f"MISSING: {path}")
        return None

    text = extract_text(path)

    row = {
        "filename": meta["filename"],
        "source": (
            default_source
            if default_source is not None
            else meta["source"]
        ),
        "year": int(meta["year"]),
        "text_type": meta.get("text_type", ""),
        "variant": meta.get("variant", ""),
        "translation": meta.get("translation", ""),
    }

    row.update(extract_features(text))
    return row


def process_collection(metadata_file, data_dir, default_source=None):
    metadata = pd.read_csv(
        metadata_file
    )

    rows = []

    for _, meta in metadata.iterrows():

        row = process_document(meta, data_dir, default_source)

        if row is not None:
            rows.append(row)

    return rows


#PROCESS CORPUS

rows = []

rows.extend(
    process_collection(CTILC_METADATA, CTILC_DIR, default_source="CTILC")
)

rows.extend(
    process_collection(EXTERNAL_METADATA, EXTERNAL_DIR)
)


#SORT

rows.sort(
    key=lambda row: (row["year"], row["source"], row["filename"])
)


#OUTPUT COLUMNS

fieldnames = [
    "filename",
    "source",
    "year",
    "text_type",
    "variant",
    "translation",
    "word_count",
]

for feature in PATTERNS:
    fieldnames.extend([
        f"{feature}_count",
        f"{feature}_freq_10k",
    ])

fieldnames.extend([
    "plural_as_count",
    "plural_as_freq_10k",
    "plural_es_count",
    "plural_es_freq_10k",
    "h_count",
    "h_freq_10k",
    "final_ch_count",
    "final_ch_freq_10k",
    "final_c_count",
    "final_c_freq_10k",
])

#SAVE

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"Written: {OUTPUT_FILE}")
print(f"Documents: {len(rows)}")
print(f"Total words: " f"{sum(row['word_count'] for row in rows):,}")