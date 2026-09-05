import pandas as pd
from scipy.stats import linregress

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
    aggregate_feature_by_period,
)

INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_FILE = "results/trend_results.csv"

#LOAD AND PREPARE DATA

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)

#ANALYZE TRENDS

results = []

for feature in FEATURES:

    grouped = aggregate_feature_by_period(df, feature)
    regression = linregress(grouped["period"], grouped["freq_per_10k"],)

    results.append({
        "feature": feature,
        "slope": regression.slope,
        "intercept": regression.intercept,
        "r_squared": regression.rvalue ** 2,
        "p_value": regression.pvalue,
        "std_error": regression.stderr,
    })

#SAVE RESULTS

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved results to {OUTPUT_FILE}\n")