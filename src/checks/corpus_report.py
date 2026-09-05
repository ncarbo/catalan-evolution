from pathlib import Path

import pandas as pd


INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_DIR = Path("results/corpus")

MIN_DOCS_PER_YEAR = 3
MIN_WORDS_PER_YEAR = 20_000
SOURCE_DOMINANCE_THRESHOLD = 0.80
TEXT_TYPE_DOMINANCE_THRESHOLD = 0.80

#LOAD DATA

df = pd.read_csv(INPUT_FILE)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#BASIC PREPARATION

df["decade"] = (df["year"] // 10) * 10

#REPORT BY YEAR

by_year = (
    df.groupby("year")
    .agg(
        documents=("filename", "count"),
        word_count=("word_count", "sum"),
    )
    .reset_index()
)

by_year.to_csv(OUTPUT_DIR / "corpus_by_year.csv", index=False)

#REPORT BY DECADE

by_decade = (
    df.groupby("decade")
    .agg(
        documents=("filename", "count"),
        word_count=("word_count", "sum"),
    )
    .reset_index()
)

by_decade.to_csv(OUTPUT_DIR / "corpus_by_decade.csv", index=False)

#REPORT BY SOURCE

by_source = (
    df.groupby("source")
    .agg(
        documents=("filename", "count"),
        word_count=("word_count", "sum"),
    )
    .reset_index()
)

by_source["document_share"] = (
    by_source["documents"]
    / by_source["documents"].sum()
)

by_source["word_share"] = (
    by_source["word_count"]
    / by_source["word_count"].sum()
)

by_source.to_csv(
    OUTPUT_DIR / "corpus_by_source.csv",
    index=False,
)

# REPORT BY TEXT TYPE

by_text_type = (
    df.groupby(
        "text_type",
        dropna=False,
    )
    .agg(
        documents=("filename", "count"),
        word_count=("word_count", "sum"),
    )
    .reset_index()
)

by_text_type["document_share"] = (
    by_text_type["documents"]
    / by_text_type["documents"].sum()
)

by_text_type["word_share"] = (
    by_text_type["word_count"]
    / by_text_type["word_count"].sum()
)

by_text_type.to_csv(
    OUTPUT_DIR / "corpus_by_text_type.csv",
    index=False,
)

#TEXT TYPE BY DECADE

text_type_decade = (
    df.groupby(
        [
            "decade",
            "text_type",
        ],
        dropna=False,
    )
    .agg(
        documents=("filename", "count"),
        word_count=("word_count", "sum"),
    )
    .reset_index()
)

decade_totals = (
    text_type_decade.groupby("decade")["word_count"]
    .transform("sum")
)

text_type_decade["word_share"] = (
    text_type_decade["word_count"]
    / decade_totals
)

text_type_decade.to_csv(
    OUTPUT_DIR / "corpus_by_decade_text_type.csv",
    index=False,
)

#DUPLICATES

duplicates = df[
    df.duplicated(
        subset=["filename"],
        keep=False,
    )
].sort_values("filename")

duplicates.to_csv(
    OUTPUT_DIR / "duplicates.csv",
    index=False,
)

#TEMPORAL GAPS

min_year = int(df["year"].min())
max_year = int(df["year"].max())

all_years = pd.DataFrame({
    "year": range(
        min_year,
        max_year + 1,
    )
})

coverage = all_years.merge(
    by_year,
    on="year",
    how="left",
)

coverage[
    [
        "documents",
        "word_count",
    ]
] = coverage[
    [
        "documents",
        "word_count",
    ]
].fillna(0)

coverage["documents"] = (
    coverage["documents"].astype(int)
)

coverage["word_count"] = (
    coverage["word_count"].astype(int)
)

#SOURCE DOMINANCE BY YEAR

source_year = (
    df.groupby(
        [ "year", "source"]
    )
    .agg(
        word_count=("word_count", "sum")
    )
    .reset_index()
)

source_totals = (
    source_year.groupby("year")[
        "word_count"
    ]
    .transform("sum")
)

source_year["share"] = (
    source_year["word_count"]
    / source_totals
)

max_source_share = (
    source_year.groupby("year")["share"]
    .max()
    .rename("max_source_share")
)

coverage = coverage.merge(
    max_source_share,
    on="year",
    how="left",
)

#TEXT TYPE DOMINANCE BY YEAR

text_type_year = (
    df.groupby(
        [
            "year",
            "text_type",
        ],
        dropna=False,
    )
    .agg(
        word_count=("word_count", "sum")
    )
    .reset_index()
)

text_type_totals = (
    text_type_year.groupby("year")[
        "word_count"
    ]
    .transform("sum")
)

text_type_year["share"] = (
    text_type_year["word_count"]
    / text_type_totals
)

max_text_type_share = (
    text_type_year.groupby("year")["share"]
    .max()
    .rename("max_text_type_share")
)

coverage = coverage.merge(
    max_text_type_share,
    on="year",
    how="left",
)

#FLAGS

coverage["missing_year"] = (
    coverage["documents"] == 0
)

coverage["low_documents"] = (
    coverage["documents"]
    < MIN_DOCS_PER_YEAR
)

coverage["low_word_count"] = (
    coverage["word_count"]
    < MIN_WORDS_PER_YEAR
)

coverage["source_dominated"] = (
    coverage["max_source_share"]
    >= SOURCE_DOMINANCE_THRESHOLD
)

coverage["text_type_dominated"] = (
    coverage["max_text_type_share"]
    >= TEXT_TYPE_DOMINANCE_THRESHOLD
)

coverage.to_csv(
    OUTPUT_DIR / "coverage_flags.csv",
    index=False,
)

#SUMMARY

summary = pd.DataFrame([
    {
        "documents": len(df),
        "word_count": df["word_count"].sum(),
        "start_year": min_year,
        "end_year": max_year,
        "sources": df["source"].nunique(),
        "text_types": df["text_type"].nunique(),
        "duplicate_rows": len(duplicates),
        "missing_years": coverage["missing_year"].sum(),
        "low_document_years": coverage["low_documents"].sum(),
        "low_word_count_years": coverage["low_word_count"].sum(),
    }
])

summary.to_csv(OUTPUT_DIR / "corpus_summary.csv", index=False)
print(f"Written corpus report to: {OUTPUT_DIR}")