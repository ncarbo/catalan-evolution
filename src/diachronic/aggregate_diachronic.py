import pandas as pd

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    normalize_frequency,
)

INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_YEAR = "data/aggregated/features_by_year.csv"
OUTPUT_DECADE = "data/aggregated/features_by_decade.csv"

df = load_diachronic_features(INPUT_FILE)

def aggregate_by_period(df, period_col):
    rows = []
    for period, group in df.groupby(period_col):

        word_count = group["word_count"].sum()

        row = {
            period_col: period,
            "documents": len(group),
            "word_count": word_count,
        }

        for feature in FEATURES:

            total_count = group[
                f"{feature}_count"
            ].sum()

            freq_10k = normalize_frequency(
                total_count,
                word_count,
            )

            row[f"{feature}_count"] = total_count
            row[f"{feature}_freq_10k"] = freq_10k

        rows.append(row)

    return pd.DataFrame(rows)


#YEAR

year_df = aggregate_by_period(df,"year")
year_df.to_csv(OUTPUT_YEAR, index=False)

#DECADE

df["decade"] = (df["year"] // 10) * 10
decade_df = aggregate_by_period(df, "decade")
decade_df.to_csv(OUTPUT_DECADE, index=False)