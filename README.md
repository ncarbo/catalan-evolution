# Diachronic Analysis of Catalan Language (1830 - 1950)

A reproducible NLP and data-analysis pipeline for studying diachronic change in written Catalan between 1832 and 1949.

The project combines a historical corpus extracted primarily from the CTILC (Corpus Textual Informatitzat de la Llengua Catalana), developed by the Institut d’Estudis Catalans, with additional texts from the Dipòsit Digital de Documents de la Universitat Autònoma de Barcelona. It extracts orthographic and lexical features and analyzes their evolution over time through trend estimation, persistence analysis, changepoint detection, linguistic oppositions, and robustness checks.

## Initial question

How did major orthographic conventions in written Catalan evolve between 1830 and 1950, particularly around the Fabrian standardization of the 1910s?

## Corpus

The corpus covers written Catalan from 1832 to 1949 and consists primarily of texts from the CTILC supplemented by a smaller number of external sources, mainly the magazines Ariel and Ressorgiment. These external texts were added to improve temporal coverage, particularly because of the limited number of documents available for the 1940s in the CTILC source

Each document is associated with metadata:

- year
- source
- text type
- linguistic variant (central, baleàric, valencià, septentrional, nord-occidental and alguerès)
- translation status
- document length

One document was excluded from the analytical metadata because it represented approximately 70% of the total word count of the 1860–1864 period, creating extreme single-document dominance. The excluded document was `002982_La_orfaneta_de_Menargues_o_Catalunya_ago.out.txt`.

## Methodology

The analytical pipeline includes:

- text cleaning, preprocessing, and metadata construction
- document-level linguistic feature extraction
- aggregation by year, decade and 5-year periods
- normalization of feature frequencies per 10,000 words
- linear trend estimation
- persistence analysis
- exploratory changepoint detection
- analysis of linguistic oppositions
- document-level robustness checks
- visualization of temporal trends and analytical results

## Main outputs

The project generates:

- document-level linguistic features
- yearly and decadal aggregated datasets
- corpus coverage and composition reports
- linear trend estimates
- persistence results
- changepoint estimates
- linguistic opposition series and crossover results
- robustness statistics comparing corpus-level and document-level frequencies
- graphical summaries of the main temporal patterns

The main generated datasets and analysis outputs are stored under `data/aggregated/` and `results/`.


## Data extraction

Publicly available CTILC texts can be retrieved using:

```bash
python3 scripts/download_all_ctilc.py
```

## Future work

Several extensions are planned for a future version of the project:

- **Document-level weighting**  

  The current analysis  relies on corpus-level frequencies, so longer documents may have greater influence. A future version could use mean document-level frequencies as the main indicator, giving each document equal weight and reducing impact of highly unequal document lengths.

- **Pre/post period prediction**  

  Train an interpretable classifier, such as logistic regression, to predict whether a document belongs to an earlier or later historical period based on its linguistic features.

- **More rigorous change-point detection**  

  Replace the current exploratory two-segment regression approach with a statistically stronger change-point. Possible extensions include penalized segmentation, model-selection criteria such as AIC/BIC or probabilistic/Bayesian change-point models.

- **Probabilistic modelling of diachronic change**  

  Move beyond purely descriptive trends toward models that explicitly represent uncertainty and temporal dynamics, allowing estimates of when changes occur and how confidently they can be identified.

- **Parallel processing and scalability experiments**

  Use the corpus-processing pipeline as a benchmark for parallel execution across multiple CPU cores, measuring runtime, speedup, efficiency, and computational bottlenecks.
