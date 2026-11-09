# CPC353 Assignment 1: project context

## Shared resources

- Repository: https://github.com/tanchinqian/CPC353-Assignment-1
- Shared Drive folder: https://drive.google.com/drive/folders/17QiiWa7heAsnfGni7v6grtXyuYeLkbOO
- Source Sheet, **English_Malay_Instant_Noodle_Review_Corpus**: https://docs.google.com/spreadsheets/d/1BzvT_kU5uHniEZFE2YcY6KccbnY7EIFWFnN0ebUUVvs/edit
- Working report, **CPC353 Assignment 1 Report - Instant Noodle Reviews**: https://docs.google.com/document/d/1-n0e8PUBgzSJbyfiynWZ8DTjAfeegzczjeHIBDEuUHg/edit
- Updated assignment guidelines: https://drive.google.com/file/d/1tem3Nenaz4oYfaaGYBu5WM1bsSgxKAfL/view
- Rubric document: https://docs.google.com/document/d/17s56Heze1OkTTV9CjTO5cMxhDMB8650Q/edit
- LaTeX bibliography folder: https://drive.google.com/drive/folders/1zqhCiH_N98vU9bMMGdIN-SvIVLlKlbgX
- IEEE template folder: https://drive.google.com/drive/folders/1J3JMfUgYx9LM7vxBR54E0hq3iOJTesQg

The shared folder contains the working report, source Sheet, guidelines, and
reference material. Re-read the current versions before editing them.

## Project scope

This shared repository contains processing code and method documentation for
the group project. Keep the report's methodology and findings consistent with
the implemented analyses. Preserve unrelated analysis components when making
changes to preprocessing, concordance, stop words, or n-grams.
The local assignment brief, collection workbook, `output/`, and `tmp/` must not
be committed. Their presence does not make them pipeline inputs.

The research question concerns product attributes in English, Malay and
code-switched instant noodle reviews. The updated guidelines require at least
one relevant NLP technique, approximately 100–200 reviews, and a 3–6 page IEEE
report excluding the cover, submitted as Word and PDF on 13 November 2026.
The group report plans concordance, n-gram and stop-word analyses. Concordance
should include KWIC examples, interpretation of surrounding language, and a
small bilingual lexicon of recurring/informal expressions.

## Data source and refresh boundary

The reproducible tracked snapshot is dated **2026-11-02**: 12 collected and 53
AI-generated Shin Ramyun reviews. All 65 are retained, with 1,201 unfiltered
tokens; 25 reviews have an inherited Code-switched label. These are snapshot
statistics, not a claim about the current live Sheet. Local collection/audit
artifacts may describe later datasets; do not mix their totals with this run.

On 2026-11-09, `Summary & Analysis!B2:F18` reports 125 live reviews: 57
collected and 68 AI, with 61 English, 28 Malay and 36 code-switched labels.
The guide and dashboard subtitle still say 65, so those descriptions are stale.
The shared report's concordance findings explicitly use the tracked 65-review
baseline; results for the live 125-review corpus require a separate refresh.

Source Sheet tabs: `Readme & Schema`, `Self-Collected Data`, `AI-Generated Data`,
and `Summary & Analysis`. Review table headings are on row 4. Use a read-only
export of the review tabs when a data refresh is requested, preserve real/AI
provenance, update `data/raw/source_snapshot.json`, then rerun preprocessing,
stop-word and concordance notebooks together. Never infer currency from the
Sheet's guide text alone. Data collection and refreshing the tracked snapshot
are separate from this concordance implementation.

## Implementation conventions and history

- `893ebc6`: separate stop-word notebook and runner support.
- `bae99d7`, `cea8809`: combined-corpus analysis rather than main results split
  by collected/AI origin.
- `dada9e5`: stop-word-related preprocessing changes.
- `3aa4b2b`: category scope broadened while documenting the single-product snapshot.

Concordance follows the same notebook-first workflow and combined-corpus
summaries. `tools/concordance.py` contains testable logic; the notebook exposes
query selection and produces evidence files. Origin and inherited language
labels stay on every hit. The code-switched subset is contextual evidence,
not automatic language identification or an origin comparison.

## Shared report destinations

The report uses tab `t.0` (Tab 1). Update by heading and freshly read text, never
by hard-coded character offsets:

- III. RELATED METHODS: add the concordance rationale alongside stop words.
- IV.B. Concordance Analysis: method and reproducibility.
- IV.E. Reliability Checks: concordance checks, clearly bounded in scope.
- V.B. Concordance Findings: measured results, identified examples and lexicon.

Use `docs/concordance_results.md` for the local evidence summary and caveats.
The report still has unfinished sections; completion of
concordance does not mean the entire assignment is ready for submission.
