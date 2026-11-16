# CPC353 Assignment 1: Instant Noodle Reviews

This project prepares and analyzes a mixed English-Malay corpus of instant noodle reviews. The current snapshot contains 125 reviews from collected and AI-generated sources. The main analyses treat them as one combined corpus while retaining source and language labels for context.

## Workflow

Run the notebooks in this order:

1. [Preprocessing](preprocessing.ipynb) prepares the review text and checks the records. It reports missing IDs or text and duplicate IDs or text, then saves an audit so exclusions can be reviewed. It normalizes and tokenizes a working copy of each review while preserving the original text and metadata. Both the unfiltered tokens and stop-word-filtered tokens are retained.
2. [Stop-word analysis](stopword_analysis.ipynb) uses the combined corpus to compare project stop-word counts before and after filtering. It also summarizes stop-word removal by review, so results are not limited to raw corpus totals.
3. [Concordance analysis](concordance_analysis.ipynb) searches unfiltered tokens for selected words and phrases. It saves keyword-in-context examples to help interpret how terms are used in their reviews.
4. [N-gram analysis](ngram_analysis.ipynb) examines adjacent two-word and three-word sequences within sentence boundaries. It compares unfiltered and filtered sequences and includes combined-corpus and contextual language or attribute views.

## Running the notebooks

Open the notebooks in Colab or Jupyter. For local use, install the core packages with `python -m pip install pandas nltk`. Keep the input CSV files in `data/raw/`, open each notebook from the project, and run its cells from top to bottom. Run preprocessing before the three analysis notebooks so they can use its saved outputs.

[Open preprocessing in Colab](https://colab.research.google.com/github/tanchinqian/CPC353-Assignment-1/blob/main/preprocessing.ipynb)

## Data and saved results

The CSV files in `data/raw/` are snapshots of the review tabs. Preprocessing writes review-level CSV and JSONL files, record audits, summaries, and a run manifest to `data/processed/`. The JSONL files preserve token arrays as arrays. The stop-word analysis saves frequency and per-review summaries under `data/analysis/`. Concordance and n-gram outputs are saved in `data/analysis/concordance/` and `data/analysis/ngram/`.

Use unfiltered tokens when the surrounding grammar or phrase context matters, including concordance and the unfiltered n-gram view. Use the filtered tokens to examine patterns after common project stop words have been removed. Neither view replaces the original review text.

See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for the snapshot details, processing decisions, and project conventions.
