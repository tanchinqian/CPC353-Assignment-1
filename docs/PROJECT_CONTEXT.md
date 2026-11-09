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
small bilingual lexicon of recurring/informal expressions. N-gram analysis
should include bigram/trigram frequencies, cross-language bigrams at
code-switching boundaries, and attribute-grouped n-gram patterns.

## Data source and refresh boundary

The reproducible tracked snapshot is dated **2026-11-09** and includes all
**125 review rows** from both shared Sheet tabs: 57 collected and 68 AI-generated
reviews across instant noodle products. All 125 survive the existing structural
and duplicate checks, with 2,252 unfiltered tokens. Inherited labels total
61 English, 28 Malay and 36 code-switched reviews.

Main analyses use the full retained corpus without contributor, ID-prefix,
product, origin or language selection. Code-switched subsets are supplementary
context views. Preserve source distinctions on records, but do not select only
one contributor's additions. The Sheet's guide/dashboard subtitle still mention
65; the actual review rows, not stale guide prose, determine the input corpus.
Local collection artifacts are not additional inputs to this run.

Source Sheet tabs: `Readme & Schema`, `Self-Collected Data`, `AI-Generated Data`,
and `Summary & Analysis`. Review table headings are on row 4. Use a read-only
export of the review tabs when a data refresh is requested, preserve real/AI
provenance, then rerun preprocessing, stop-word, concordance and n-gram notebooks
together. `tools/refresh_snapshot.py` imports a complete connector values JSON
export, saves review candidates and source row numbers, and updates
`data/raw/source_snapshot.json` with counts, ranges and hashes. The export JSON
stays local; the existing tracked CSV snapshots and processing outputs are
refreshed together. Never infer currency from the Sheet's guide text alone.

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

- III. RELATED METHODS: add concordance and n-gram rationales alongside stop words.
- IV.B. Concordance Analysis: method and reproducibility.
- IV.C. N-gram Analysis: bigram/trigram extraction and cross-language boundaries.
- IV.E. Reliability Checks: concordance and n-gram checks, clearly bounded in scope.
- V.B. Concordance Findings: measured results, identified examples and lexicon.
- V.C. N-gram Findings: frequent collocations and directional code-switching patterns.

For a full-corpus refresh also update II. Scenario and Dataset, V.A. Corpus
Overview, V.C. N-gram Findings, and V.D. Stop-Word Findings including their native tables. Preserve
unrelated writing, author information and the completed n-gram sections.

Use `docs/concordance_results.md` for the local evidence summary and caveats.
The report still has unfinished sections; completion of
concordance and n-gram analyses does not mean the entire assignment is ready for submission.

### Report visuals

The shared report contains editable native tables and a workflow figure,
using the full 2026-11-09 snapshot:

- Figure 1: all 125 review rows, preprocessing, then concordance, n-gram and
  stop-word analysis, with matching solid borders for all three branches.
  This is an overview of the report methods; n-gram implementation is provided in
  `ngram_analysis.ipynb`.
- Table I: language counts by collected/AI origin, with totals.
- Table II: selected concordance terms, meanings, occurrences and review coverage.
- Table III: short collected-review excerpts with contextual interpretation.
- Table IV: the five most frequent project stop words and normalized counts.

Figure 1 uses an input parallelogram, rectangular process boxes, and directional
arrows. Its three branches share the preprocessed corpus; they are not a decision
or a sequential dependency. The editable vector source is
`docs/figures/analysis_workflow.svg` (234 x 186 pt). Insert a high-resolution PNG
render at that size in the report, with the figure caption below it. Generated
image exports belong in ignored `output/`, not in Git.

Review identifiers stay in supporting evidence, not visual captions or report
prose. Tables fit one IEEE column (234 pt), with 9 pt Times New Roman text and
light gray headers; body text is 10 pt. Methodology and results start on new
pages to keep the current visuals intact. Recheck pagination after content
changes. The visually checked export has five pages including the cover;
remaining assignment placeholders are not completed by these layout changes.
