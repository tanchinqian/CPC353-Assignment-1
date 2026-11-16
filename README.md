# CPC353 Assignment 1: Instant Noodle Reviews

This project prepares and analyzes a mixed English-Malay corpus of instant noodle reviews. The current snapshot has 125 collected and AI-generated reviews. Main analyses use the combined corpus.

## Run the notebooks

Run preprocessing first, then run the analysis notebooks:

1. [Preprocessing](preprocessing.ipynb)
2. [Stop-word analysis](stopword_analysis.ipynb)
3. [Concordance analysis](concordance_analysis.ipynb)
4. [N-gram analysis](ngram_analysis.ipynb)

Open the notebooks in Colab or Jupyter. For local use, install Python packages with `python -m pip install pandas nltk`. Keep the input CSV files in `data/raw/` and run all cells.

[Open preprocessing in Colab](https://colab.research.google.com/github/tanchinqian/CPC353-Assignment-1/blob/main/preprocessing.ipynb)

## Data and results

The notebooks preserve the original review text and unfiltered tokens. Preprocessing saves cleaned data, audit files, and a run manifest in `data/processed/`. Stop-word analysis compares the combined corpus before and after filtering. Concordance uses unfiltered tokens. N-gram analysis saves its results in `data/analysis/ngram/`; other analysis results are saved in `data/analysis/`.

The tracked CSV files in `data/raw/` are snapshots of the review tabs. See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for snapshot details and project conventions.
