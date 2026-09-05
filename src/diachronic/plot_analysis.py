from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
    aggregate_feature_by_period,
)


INPUT_FEATURES = "data/features/features_diachronic.csv"
INPUT_TRENDS = "results/trend_results.csv"
INPUT_CHANGEPOINTS = "results/changepoint_results.csv"
OUTPUT_DIR = Path("results/plots_analysis")


#LOAD DATA

df = load_diachronic_features(INPUT_FEATURES)
df = add_period(df)
trends = pd.read_csv(INPUT_TRENDS)
changepoints = pd.read_csv(INPUT_CHANGEPOINTS)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#PLOT EACH FEATURE

for feature in FEATURES:

    grouped = aggregate_feature_by_period(df, feature)

    trend_row = trends[
        trends["feature"] == feature
    ].iloc[0]

    changepoint_row = changepoints[
        changepoints["feature"] == feature
    ].iloc[0]

    slope = trend_row["slope"]
    intercept = trend_row["intercept"]
    breakpoint = changepoint_row["breakpoint"]

    #Predicted values from the global linear regression
    predicted = (intercept + slope * grouped["period"])


    #CREATE PLOT

    plt.figure(figsize=(10, 5))

    #Observed frequencies
    plt.plot(
        grouped["period"],
        grouped["freq_per_10k"],
        marker="o",
        label="Observed",
    )

    # Global linear trend
    plt.plot(
        grouped["period"],
        predicted,
        linestyle="--",
        label="Linear trend",
    )

    # Detected changepoint
    plt.axvline(
        x=breakpoint,
        linestyle=":",
        label=f"Breakpoint: {int(breakpoint)}",
    )

    plt.title(feature)
    plt.xlabel("Period")
    plt.ylabel("Frequency per 10,000 words")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    #SAVE PLOT

    plt.savefig(
        OUTPUT_DIR / f"{feature}_analysis.png",
        dpi=150,
    )

    plt.close()