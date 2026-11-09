# Project handoff

Read `docs/PROJECT_CONTEXT.md` and `README.md` before changing the pipeline.
Keep this shared repository focused on processing code, tests, notebook
explanations, and method documentation.

Do not commit the local assignment brief, collection-schema spreadsheet,
`output/`, or `tmp/`. They are reference/collection artifacts, not repository
deliverables. Generated concordance tables belong in the ignored directory
`data/analysis/concordance/`; reproduce them with the notebook. Do not add them
with `git add -f`. Existing tracked corpus snapshots remain in place.

Preserve original reviews, origin labels, and provenance. Use unfiltered
sentence tokens for concordance; never merge separate reviews. Report exactly
which snapshot was analyzed. Do not silently replace raw data from the live
Sheet or treat synthetic examples as verified customer statements.

Use the full retained corpus from both source review tabs for the main analyses.
Do not restrict inputs by contributor, review-ID prefix, product or language.
Apply the documented missing-data and duplicate checks uniformly; keep any
exclusions in the audit. Language subsets are supplementary context views.

Run `python -m unittest discover -s tests -p test_concordance.py` and
`python tools/run_notebook.py concordance_analysis.ipynb` after concordance
changes. For preprocessing changes also run `python tests/check_preprocessing.py`.

Shared resources and report section locations are in `docs/PROJECT_CONTEXT.md`.
Read the live report before editing and preserve unrelated sections. Do not
replace the entire report for a concordance update. Refresh corpus outputs and
report evidence together; never keep old numerical conclusions after changing
the inputs or query configuration.
