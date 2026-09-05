import pandas as pd

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
)

INPUT_FILE = "data/features/features_diachronic.csv"

OUTPUT_PERIOD = "results/robustness_by_period.csv"
OUTPUT_DOMINANT = "results/dominant_documents.csv"

# LOAD AND PREPARE DATA

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)

robustness_rows = []
dominant_rows = []

# ANALYZE EACH FEATURE

for feature in FEATURES:

    freq_col = f"{feature}_freq_10k"
    count_col = f"{feature}_count"

    for period, group in df.groupby("period"):

        total_words = group["word_count"].sum()
        total_count = group[count_col].sum()

        # Global frequency:
        # large documents have more weight
        global_freq = (
            total_count / total_words * 10_000
            if total_words > 0
            else 0
        )

        # Document-level distribution:
        # each document has equal weight
        mean_document_freq = group[freq_col].mean()
        median_document_freq = group[freq_col].median()
        std_document_freq = group[freq_col].std()

        q25 = group[freq_col].quantile(0.25)
        q75 = group[freq_col].quantile(0.75)

        robustness_rows.append({
            "feature": feature,
            "period": period,
            "documents": len(group),
            "word_count": total_words,

            "global_freq": global_freq,
            "mean_document_freq": mean_document_freq,
            "median_document_freq": median_document_freq,
            "std_document_freq": std_document_freq,

            "q25": q25,
            "q75": q75,
        })


# DOMINANT DOCUMENTS BY PERIOD

for period, group in df.groupby("period"):

    total_words = group["word_count"].sum()

    if total_words == 0:
        continue

    largest_document = group.loc[group["word_count"].idxmax()]

    largest_share = (largest_document["word_count"] / total_words)

    dominant_rows.append({
        "period": period,
        "filename": largest_document["filename"],
        "source": largest_document["source"],
        "word_count": largest_document["word_count"],
        "period_word_count": total_words,
        "largest_document_share": largest_share,
    })


# SAVE RESULTS

robustness_df = pd.DataFrame(robustness_rows)
dominant_df = pd.DataFrame(dominant_rows)

robustness_df.to_csv(OUTPUT_PERIOD, index=False)
dominant_df.to_csv(OUTPUT_DOMINANT, index=False)