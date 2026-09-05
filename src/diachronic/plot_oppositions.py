from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

INPUT_SERIES = "results/opposition_series.csv"
INPUT_RESULTS = "results/opposition_results.csv"
OUTPUT_DIR = Path("results/plots_oppositions")

#LOAD RESULTS

series = pd.read_csv(INPUT_SERIES)
results = pd.read_csv(INPUT_RESULTS)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# PLOT EACH OPPOSITION

for opposition in series["opposition"].unique():

    data = series[
        series["opposition"] == opposition
    ].copy()

    result = results[
        results["opposition"] == opposition
    ].iloc[0]

    left_label = result["left_features"]
    right_label = result["right_features"]

    crossover = result["permanent_crossover_period"]

    # CREATE PLOT

    plt.figure(figsize=(10, 5))

    # Left form
    plt.plot(
        data["period"],
        data["left_freq_per_10k"],
        marker="o",
        label=left_label,
    )

    # Right form
    plt.plot(
        data["period"],
        data["right_freq_per_10k"],
        marker="o",
        label=right_label,
    )


    # CROSSOVER

    if pd.notna(crossover):

        plt.axvline(
            x=crossover,
            linestyle=":",
            label=f"Permanent crossover: {int(crossover)}"
        )


    # FORMAT

    plt.title(opposition.replace("_", " "))

    plt.xlabel("Period")
    plt.ylabel("Frequency per 10,000 words")

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()


    # SAVE

    plt.savefig(OUTPUT_DIR / f"{opposition}.png", dpi=150)

    plt.close()