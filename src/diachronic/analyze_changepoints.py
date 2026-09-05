import pandas as pd
import numpy as np
from scipy.stats import linregress

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
    aggregate_feature_by_period,
)

INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_FILE = "results/changepoint_results.csv"

MIN_POINTS_PER_SEGMENT = 3

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)

#FUNCTION: REGRESSION ERROR

def regression_sse(x, y):
    result = linregress(x, y)
    predicted = (result.intercept + result.slope * x)
    sse = np.sum((y - predicted) ** 2)
    return sse, result.slope

#SIMPLE TWO-SEGMENT CHANGEPOINT ANALYSIS
#We establish the analysis in two segments

all_results = []

for feature in FEATURES:
    count_col = f"{feature}_count"

    #AGGREGATE BY 5-YEAR PERIOD

    grouped = aggregate_feature_by_period(df, feature)

    x = grouped["period"].to_numpy()
    y = grouped["freq_per_10k"].to_numpy()

    #INITIAL VALUES

    best_breakpoint = None
    best_sse = np.inf
    best_left_slope = None
    best_right_slope = None

    #TRY EVERY POSSIBLE BREAKPOINT

    for i in range(MIN_POINTS_PER_SEGMENT, len(grouped) - MIN_POINTS_PER_SEGMENT):

        x_left = x[:i]
        y_left = y[:i]
        x_right = x[i:]
        y_right = y[i:]

        left_sse, left_slope = regression_sse(x_left, y_left)
        right_sse, right_slope = regression_sse(x_right, y_right)
        total_sse = (left_sse + right_sse)

        if total_sse < best_sse:
            best_sse = total_sse
            best_breakpoint = x[i]
            best_left_slope = left_slope
            best_right_slope = right_slope

    #SAVE RESULT

    all_results.append({
        "feature": feature,
        "breakpoint": best_breakpoint,
        "slope_before": best_left_slope,
        "slope_after": best_right_slope,
        "sse": best_sse,
    })

#SAVE CSV

results_df = pd.DataFrame(all_results)
results_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved results to " f"{OUTPUT_FILE}\n")