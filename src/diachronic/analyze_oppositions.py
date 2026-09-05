import pandas as pd
from scipy.stats import linregress

from utils_diachronic import (
    load_diachronic_features,
    add_period,
    aggregate_feature_group_by_period,
)


INPUT_FILE = "data/features/features_diachronic.csv"

OUTPUT_SUMMARY = "results/opposition_results.csv"
OUTPUT_SERIES = "results/opposition_series.csv"


OPPOSITIONS = {
    "y_vs_i": {
        "left": ["y"],
        "right": ["i"],
    },

    "ab_vs_amb": {
        "left": ["ab"],
        "right": ["amb"],
    },

    "lo_los_vs_el_els": {
        "left": ["lo", "los"],
        "right": ["el", "els"],
    },

    "a_acute_vs_a_grave": {
        "left": ["a_acute"],
        "right": ["a_grave"],
    },

    "plural_as_vs_plural_es": {
        "left": ["plural_as"],
        "right": ["plural_es"],
    },

    "final_ch_vs_final_c": {
        "left": ["final_ch"],
        "right": ["final_c"],
    },
}


# LOAD AND PREPARE DATA

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)


summary_rows = []
series_rows = []

#ANALYZE EACH OPPOSITION

for opposition_name, opposition in OPPOSITIONS.items():

    left_features = opposition["left"]
    right_features = opposition["right"]

    left = aggregate_feature_group_by_period(df, left_features)
    right = aggregate_feature_group_by_period(df, right_features)

    # MERGE BOTH TEMPORAL SERIES

    comparison = left[
        ["period", "freq_per_10k"]
    ].rename(
        columns={
            "freq_per_10k": "left_freq_per_10k"
        }
    )

    comparison = comparison.merge(
        right[
            ["period", "freq_per_10k"]
        ].rename(
            columns={
                "freq_per_10k": "right_freq_per_10k"
            }
        ),
        on="period",
    )


    #DIFFERENCE BETWEEN BOTH FORMS

    comparison["difference"] = (
        comparison["left_freq_per_10k"]
        - comparison["right_freq_per_10k"]
    )


    #GLOBAL LINEAR TRENDS

    left_regression = linregress(comparison["period"], comparison["left_freq_per_10k"],)
    right_regression = linregress(comparison["period"], comparison["right_freq_per_10k"],)


    # FIRST PERMANENT CROSSOVER

    crossover_period = None

    for i in range(len(comparison)):

        remaining = comparison.iloc[i:]

        if (remaining["right_freq_per_10k"] >= remaining["left_freq_per_10k"]).all():

            crossover_period = int(comparison.iloc[i]["period"])

            break

    # SAVE FULL TEMPORAL SERIES

    for _, row in comparison.iterrows():

        series_rows.append({
            "opposition": opposition_name,
            "period": int(row["period"]),
            "left_freq_per_10k": row["left_freq_per_10k"],
            "right_freq_per_10k": row["right_freq_per_10k"],
            "difference": row["difference"],
        })

    # SAVE SUMMARY

    summary_rows.append({
        "opposition": opposition_name,

        "left_features": "+".join(left_features),
        "right_features": "+".join(right_features),

        "left_slope": left_regression.slope,
        "left_r_squared": left_regression.rvalue ** 2,
        "left_p_value": left_regression.pvalue,

        "right_slope": right_regression.slope,
        "right_r_squared": right_regression.rvalue ** 2,
        "right_p_value": right_regression.pvalue,

        "permanent_crossover_period": crossover_period,

        "left_start": comparison.iloc[0]["left_freq_per_10k"],
        "left_end": comparison.iloc[-1]["left_freq_per_10k"],

        "right_start": comparison.iloc[0]["right_freq_per_10k"],
        "right_end": comparison.iloc[-1]["right_freq_per_10k"],
    })


# SAVE RESULTS

summary_df = pd.DataFrame(summary_rows)
series_df = pd.DataFrame(series_rows)
summary_df.to_csv(OUTPUT_SUMMARY, index=False)
series_df.to_csv(OUTPUT_SERIES, index=False)