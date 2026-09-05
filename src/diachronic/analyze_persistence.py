import pandas as pd

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
    aggregate_feature_by_period,
)

INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_FILE = "results/persistence_results.csv"

BASELINE_END = 1899
THRESHOLDS = [0.20, 0.25, 0.30, 0.40]
MIN_CONSECUTIVE_PERIODS = 3

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)

all_results = [] 

for feature in FEATURES:

    grouped = aggregate_feature_by_period(df,feature)

    #BASELINE

    baseline_data = grouped[grouped["period"] <= BASELINE_END]
    baseline = baseline_data["freq_per_10k"].mean()
    grouped["relative_to_baseline"] = (grouped["freq_per_10k"] / baseline)
    results = []

    #TEST DIFFERENT THRESHOLDS

    for threshold in THRESHOLDS:

        grouped["below_threshold"] = (grouped["relative_to_baseline"] < threshold)

        #SUSTAINED LOW LEVEL

        sustained_low_start = None

        for i in range(len(grouped) - MIN_CONSECUTIVE_PERIODS + 1):

            window = grouped.iloc[i:i + MIN_CONSECUTIVE_PERIODS]

            if window["below_threshold"].all():
                sustained_low_start = grouped.iloc[i]["period"]
                break

        #PERMANENT LOW LEVEL

        permanent_low_start = None

        for i in range(len(grouped)):

            remaining = grouped.iloc[i:]

            if remaining["below_threshold"].all():
                permanent_low_start = grouped.iloc[i]["period"]
                break

        #SAVE RESULT FOR THIS THRESHOLD

        results.append({
            "threshold": threshold,
            "sustained": sustained_low_start,
            "permanent": permanent_low_start,
        })

    #OUTPUT

    for result in results:

        all_results.append({
            "feature": feature,
            "baseline": baseline,
            "threshold": result["threshold"],
            "sustained_start": result["sustained"],
            "permanent_start": result["permanent"],
        })

#SAVE CSV

results_df = pd.DataFrame(all_results)
results_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved results to {OUTPUT_FILE}\n")