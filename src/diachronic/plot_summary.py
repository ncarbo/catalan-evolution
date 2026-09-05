from pathlib import Path

import matplotlib.pyplot as plt

from utils_diachronic import (
    FEATURES,
    load_diachronic_features,
    add_period,
    aggregate_feature_by_period,
)

INPUT_FILE = "data/features/features_diachronic.csv"
OUTPUT_DIR = Path("results/plots")

#LOAD AND PREPARE DATA

df = load_diachronic_features(INPUT_FILE)
df = add_period(df)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

#PLOT EACH FEATURE

for feature in FEATURES:

    grouped = aggregate_feature_by_period(df, feature)
    
    plt.figure(figsize=(10, 5))
    plt.plot(
        grouped["period"],
        grouped["freq_per_10k"],
        marker="o",
    )

    plt.title(feature)
    plt.xlabel("Period")
    plt.ylabel("Frequency per 10,000 words")

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{feature}.png",
        dpi=150,
    )

    plt.close()