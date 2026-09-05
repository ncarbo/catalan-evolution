import pandas as pd

START_YEAR = 1832
END_YEAR = 1949
PERIOD_SIZE = 5
FREQUENCY_SCALE = 10_000

FEATURES = [
    # Historical alternatives
    "y",
    "i",

    "ab",
    "amb",

    "lo",
    "los",
    "el",
    "els",

    # Accents
    "a_acute",
    "a_grave",

    # Orthographic sequences
    "cedilla",
    "ny",
    "ss",
    "qu_diaeresis",

    # Token-based features
    "plural_as",
    "plural_es",

    "h",

    "final_ch",
    "final_c",
]

def load_diachronic_features(
    path,
    start_year=START_YEAR,
    end_year=END_YEAR,
):
    
#    Load diachronic document-level features and restrict
#    them to the study period.
    
    df = pd.read_csv(path)

    return df[
        (df["year"] >= start_year)
        & (df["year"] <= end_year)
    ].copy()


def add_period(
    df,
    period_size=PERIOD_SIZE,
    year_col="year",
    period_col="period",
):
#   Assign each year to a fixed-width temporal period.

    df = df.copy()

    df[period_col] = (
        df[year_col] // period_size
    ) * period_size

    return df


def normalize_frequency(
    count,
    total_words,
    scale=FREQUENCY_SCALE,
):
    
#   Normalize a raw count by corpus size.
    
    if total_words == 0:
        return 0.0

    return count / total_words * scale


def aggregate_feature_by_period(
    df,
    feature,
    period_col="period",
    scale=FREQUENCY_SCALE,
):
    
#   Aggregate a linguistic feature over temporal periods.
    
    count_col = f"{feature}_count"

    grouped = (
        df.groupby(period_col)
        .agg(
            total_count=(count_col, "sum"),
            total_words=("word_count", "sum"),
        )
        .reset_index()
    )

    grouped["freq_per_10k"] = (
        grouped["total_count"]
        / grouped["total_words"]
        * scale
    )

    return grouped

def aggregate_feature_group_by_period(
    df,
    features,
    period_col="period",
    scale=FREQUENCY_SCALE,
):
    """
    Aggregate the combined counts of several features
    over temporal periods.
    """

    grouped = (
        df.groupby(period_col)
        .agg(
            total_words=("word_count", "sum"),
        )
        .reset_index()
    )

    total_counts = None

    for feature in features:

        feature_counts = (
            df.groupby(period_col)[f"{feature}_count"]
            .sum()
            .reset_index(name=f"{feature}_count")
        )

        grouped = grouped.merge(
            feature_counts,
            on=period_col,
        )

        if total_counts is None:
            total_counts = grouped[f"{feature}_count"].copy()
        else:
            total_counts += grouped[f"{feature}_count"]

    grouped["total_count"] = total_counts

    grouped["freq_per_10k"] = (
        grouped["total_count"]
        / grouped["total_words"]
        * scale
    )

    return grouped[
        [
            period_col,
            "total_count",
            "total_words",
            "freq_per_10k",
        ]
    ]