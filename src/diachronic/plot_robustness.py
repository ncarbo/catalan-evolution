from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

INPUT_FILE = "results/robustness_by_period.csv"
OUTPUT_DIR = Path("results/plots_robustness")

#LOAD DATA

df = pd.read_csv(INPUT_FILE)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


#PLOT EACH FEATURE

for feature in df["feature"].unique():

    data = df[df["feature"] == feature].copy()
    plt.figure(figsize=(10, 5))

    #GLOBAL FREQUENCY
    #Each word has equal weight

    plt.plot(
        data["period"],
        data["global_freq"],
        marker="o",
        label="Global frequency",
    )


    #MEAN DOCUMENT FREQUENCY
    #Each document has equal weight

    plt.plot(
        data["period"],
        data["mean_document_freq"],
        marker="o",
        linestyle="--",
        label="Mean document frequency",
    )


    #MEDIAN DOCUMENT FREQUENCY

    plt.plot(
        data["period"],
        data["median_document_freq"],
        linestyle=":",
        label="Median document frequency",
    )


    #INTERQUARTILE RANGE
    #Middle 50% of document frequencies

    plt.fill_between(
        data["period"],
        data["q25"],
        data["q75"],
        alpha=0.2,
        label="Document IQR",
    )


    #FORMAT

    plt.title(f"Robustness analysis: {feature}")

    plt.xlabel("Period")
    plt.ylabel("Frequency per 10,000 words")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()


    #SAVE

    plt.savefig(
        OUTPUT_DIR / f"{feature}_robustness.png",
        dpi=150,
    )

    plt.close()