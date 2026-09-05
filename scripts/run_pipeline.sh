#!/bin/bash
set -e

python3 src/features/extract_diachronic_features.py
python3 src/diachronic/aggregate_diachronic.py
python3 src/checks/corpus_report.py

python3 src/diachronic/analyze_trends.py
python3 src/diachronic/analyze_persistence.py
python3 src/diachronic/analyze_changepoints.py
python3 src/diachronic/analyze_oppositions.py
python3 src/diachronic/analyze_robustness.py

python3 src/diachronic/plot_summary.py
python3 src/diachronic/plot_analysis.py
python3 src/diachronic/plot_oppositions.py
python3 src/diachronic/plot_robustness.py