# CPC353 Assignment 1 — Shin Ramyun corpus

Start with **[preprocessing.ipynb](preprocessing.ipynb)**. It prepares the
English-Malay reviews while preserving original text and unfiltered tokens.
Then run **[stopword_analysis.ipynb](stopword_analysis.ipynb)** for the
stop-word frequency analysis. The notebooks use pandas; preprocessing also
uses NLTK without resource downloads.

[Open in Colab](https://colab.research.google.com/github/tanchinqian/CPC353-Assignment-1/blob/main/preprocessing.ipynb)

## Run

1. Open the notebook in Colab/Jupyter.
2. Install `requirements.txt` locally, or run `%pip install pandas nltk` in Colab.
3. Keep the two CSV inputs under `data/raw/` and set `PROJECT_DIR` in cell 1.
4. Run every cell in `preprocessing.ipynb` in order, then run `stopword_analysis.ipynb`.
5. Use `data/processed/` and `data/analysis/` for saved outputs. Download `preprocessed_results.zip`
   or set the project folder to mounted Drive before the Colab session ends.

A local command runs a selected notebook and saves its outputs:

```powershell
python -m pip install -r requirements.txt
python tools/run_notebook.py preprocessing.ipynb
python tools/run_notebook.py stopword_analysis.ipynb
```

The runner uses a shared Python namespace, not a Jupyter kernel; the notebook
contains ordinary Python and can also run interactively. Package versions in
requirements match the tested local environment.

## Input and refresh

The CSV files are read-only value snapshots of the two review tabs in
[the source workbook](https://docs.google.com/spreadsheets/d/1BzvT_kU5uHniEZFE2YcY6KccbnY7EIFWFnN0ebUUVvs/edit).
They preserve original text, source metadata, annotations and AI provenance.
See `data/raw/source_snapshot.json`. Only review-bearing rows are copied;
blank/template/prompt-only rows are omitted.

For more reviews, replace the appropriate CSV with an updated export, keeping
its headings. Alternatively set `WORKBOOK` to a freshly exported XLSX in the
notebook and install `openpyxl`; it reads headings on row 4 of
`Self-Collected Data` and `AI-Generated Data`. This optional XLSX route has
not been executed locally because openpyxl is unavailable. Add the workbook
locally without committing it unless needed. No Google credentials or APIs
are required to run the notebook, and it never writes to the Google Sheet.

## Processing decisions

- Unit: a complete review. Origins remain `real` and `ai`; “real” denotes
  collected origin and does not independently verify a source.
- Preserve original wording and metadata. Process only the review column,
  never prompt strategies, notes, IDs or dates.
- Check missing IDs/text and repeated IDs within an origin. Exclude all
  repeated-ID rows until resolved, rather than arbitrarily choosing one.
- Remove duplicate text after NFKC/case/apostrophe/dash/whitespace normalization.
  Keep the first structurally valid row, with real data before AI. No fuzzy
  duplicate removal. Each exclusion is recorded in `review_audit.csv`.
- Manual exclusions require origin, ID and exact original-text SHA-256.
  Prior exclusions from the old multi-product dataset are not transferred.
- On a derived copy, decode HTML entities, lowercase, normalize Unicode,
  remove URLs/emails/HTML tags and collapse whitespace.
- NLTK RegexpTokenizer keeps letter-based Unicode words, contractions, internal
  hyphens and trailing digits. Punctuation, emojis and standalone numbers stay
  in originals but are excluded from lexical tokens.
- Preserve abbreviations, repeated letters and code-switching. No stemming,
  lemmatization, translation or spelling correction.
- Save approximate sentence-token arrays split on . ! ? and ellipsis.
  This is a transparent rule, not a language-aware sentence model; manually
  check abbreviations and contexts when interpreting results.
- Use one conservative, project-authored English–Malay stop-word list,
  exported with item-level reasons. It is not a standard Malay list or the
  full NLTK English list. Retain negation, contrast markers, intensifiers and
  discourse particles. Keep both pre-filter and filtered tokens.
- Keep existing language/switching labels. Product names alone do not prove
  switching; group review of annotations remains necessary.
- Dates/ratings are metadata, not preprocessing features. Assigned real dates
  are synthetic, not original publication dates.

## Saved outputs

| File in data/processed | Purpose |
| --- | --- |
| real_preprocessed / ai_preprocessed (.csv and .jsonl) | All structurally retained reviews, separately by origin |
| real_codeswitched / ai_codeswitched (.csv and .jsonl) | Existing code-switched labels only |
| review_audit.csv | Every candidate row, original text, inclusion and exclusion reasons |
| manual_review_queue.csv | Metadata/source warnings requiring human checks |
| cleaning_summary.csv | Reviews before/after, exclusions and token totals per origin |
| language_counts.csv | Retained review count per origin and language |
| stopwords_used.csv / protected_words.csv | Exact list and preservation choices |
| run_manifest.json | Input SHA-256, Python/package versions, counts and decisions |

JSONL preserves actual arrays. CSV array cells are JSON strings:
`json.loads(cell)`, never `eval(cell)`.

For **stop-word analysis**, compare `tokens_before`, `tokens_after` and
`tokens_removed`. Preprocessing does not delete original wording or the
unfiltered token list. The separate `stopword_analysis.ipynb` compares
stop-word frequencies and saves tables under `data/analysis/`.

Filtering does not delete the original review or the unfiltered token list.
Each JSONL row keeps `original_text`, `tokens_before`, `tokens_after` and
`tokens_removed`. Use the original text for meaning and the unfiltered tokens
for concordance and n-grams. Use the filtered tokens to see which words stand
out when common grammatical words are omitted. For example, if `dan` is on the
stop-word list, it is removed from the filtered view; `tak` and `not` are kept
because negation changes meaning. The exact list is in `stopwords_used.csv`.

In the later stop-word analysis, count words in the before and after views,
using the full dataset as one corpus. For example:

```python
from collections import Counter
import json
from pathlib import Path

all_rows = []
for filename in ["real_preprocessed.jsonl", "ai_preprocessed.jsonl"]:
    all_rows.extend(json.loads(line) for line in
                    Path("data/processed", filename).read_text(encoding="utf-8").splitlines())
before_counts = Counter(token for row in all_rows for token in row["tokens_before"])
after_counts = Counter(token for row in all_rows for token in row["tokens_after"])
print(after_counts.most_common(20))
```

Compare these counts to see which words recur and how much filtering changes
the full corpus. A word count alone does not prove an attribute is frequently
discussed. The corpus contains both collected and AI-generated reviews, so
describe it as a mixed-source dataset rather than treating every review as a
verified customer account.

The stop-word notebook saves these combined-corpus tables:

| File in data/analysis | Purpose |
| --- | --- |
| stopword_frequency_overall.csv | Frequency of each project stop word before and after filtering, including normalized rates |
| stopword_review_summary.csv | Stop-word counts and removed-token share for each review |

## Assignment requirements and current limitations

The brief's data-preparation requirements are covered: originals retained,
missing entries/duplicates addressed, unit defined, before/after counts saved,
and datasets reusable. The brief asks for approximately 100–200 reviews and
a 3–6 page IEEE report (excluding cover), Word and PDF, due 13 November 2026.
This deliverable is preprocessing; it does not claim to complete the report
or the three final analyses.

Current snapshot: **12 collected + 53 AI = 65 reviews**, below the target.
Preprocessing currently retains all 65 structurally valid unique texts.
Collected labels: 7 English, 5 code-switched. AI labels: 16 English,
17 Malay, 20 code-switched. Treat counts as provisional.

REV-01 mentions duck seasoning despite its Shin Ramyun product metadata:
check the source/content before final analysis. It is flagged, not silently
deleted. The pipeline does not verify any website; resolve the manual queue
before publishing final findings.

The AI examples were generated from themes, without direct real-review seed
IDs. The brief permits generation from a real seed set: confirm whether this
theme-based approach is acceptable or regenerate from verified Shin Ramyun
seed reviews later. No seed provenance is invented.

The supplied reference notebook is used for its simple preprocessing layout,
not its classifier or depression dataset:
https://colab.research.google.com/drive/1ykOKZZuW_DmxB8iLKAn9OT2E812foMCg

Method documentation:
https://www.nltk.org/api/nltk.tokenize.regexp.html
https://www.nltk.org/book/ch02.html

## Validation

The notebook checks original-text hashes, unique IDs, preserved negations,
contractions, informal forms, URL/email removal, sentence boundaries, token
order/count reconciliation and exported JSONL round trips.
`tests/check_preprocessing.py` exercises missing records, duplicate IDs/text,
origin priority and source warnings using small fixtures.
