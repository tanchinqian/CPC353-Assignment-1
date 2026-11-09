# Concordance: method and snapshot findings

## Scope and reproduction

This analysis uses the complete **2026-11-09** source Sheet snapshot across
instant noodle products. All 125 review candidates (57 collected, 68
AI-generated) pass the existing structural and duplicate checks and contribute
2,252 unfiltered tokens. Inherited labels are 61 English, 28 Malay and 36
code-switched reviews. There is no contributor, ID-prefix, product, origin or
language selection. Blank/template/prompt-only rows are not review candidates.

Run `python tools/run_notebook.py concordance_analysis.ipynb` from the repository.
The ignored `data/analysis/concordance/` directory contains complete KWIC,
keyword coverage, lexicon evidence and a hash manifest. Inputs are the two
preprocessed JSONL files generated from refreshed raw CSV snapshots. All four
implemented notebooks were rerun together; the live source Sheet was read only.
Shared report and resource URLs are in `PROJECT_CONTEXT.md`.

## Method

The notebook combines all retained collected and AI-generated reviews. It selects English and Malay words related to product attributes, evaluation and contrast, together with frequent words from the corpus. This produces 37 search terms, including phrases such as “not too spicy”. Each match is displayed with up to five words on either side, within the same sentence. Stop words remain in these context lines so that negation and other relationships between words are preserved.

For each term, the notebook records its frequency and the number of reviews containing it. Matching ignores letter case but keeps forms such as “kuah” and “kuahnya” separate. The results are saved as “kwic.csv” and “keyword_summary.csv” in the concordance analysis folder. A small bilingual lexicon explains selected expressions and informal spellings. The original reviews remain available for checking meaning and switches between sentences.

The search combines 32 specified queries and 12 frequency-selected candidates, giving 37 distinct queries and 332 matches. Frequency ties are alphabetical. Candidate ranking excludes the project stop words and six listed product-name tokens, while the searched context remains unfiltered. Overlapping matches are retained. Different queries can match the same passage; 332 matches does not mean 332 independent passages. Full parameters are recorded in the notebook and run manifest.

## Findings

In the combined corpus of 125 reviews, “kuah” occurred 21 times in 18 reviews and “sedap” occurred 20 times in 19 reviews. The texture terms “kenyal” and “springy” appeared ten and six times, respectively. These words provide starting points for examining broth, taste and texture. Their surrounding words show how the attributes are evaluated.

One collected review describes the noodles as “not too spicy” but says the soup taste is not “kaw”. The negation qualifies the heat level and expresses a separate criticism of the soup’s flavour. Another collected review says, “Tak perlu goreng just rebus atau celur mi”. The English word “just” appears within Malay preparation advice, showing how code-switching is used to describe convenience.

The bilingual lexicon records meanings such as “sedap” (tasty) and “kenyal” (springy or chewy), alongside informal forms such as “mmg” (memang) and “sgt” (sangat). Each abbreviation occurred twice in collected reviews. Keeping these forms makes the informal wording available for analysis. Together, the examples show how attributes are described and qualified in mixed-language text. The findings describe this combined collected and AI-generated corpus, rather than customer preferences across all instant noodle products.

## Supporting evidence

Review identifiers remain here and in the exported evidence files for tracing examples; they are omitted from the report prose.

| Query | Occurrences | Distinct reviews | Code-switched-labelled reviews containing it |
| --- | ---: | ---: | ---: |
| sedap | 20 | 19 | 9 |
| kuah | 21 | 18 | 10 |
| broth | 10 | 9 | 1 |
| kenyal | 10 | 10 | 3 |
| tak | 13 | 12 | 8 |
| springy | 6 | 6 | 3 |
| tapi | 4 | 4 | 4 |

These are exact-query counts, not aggregated attribute frequencies. A matched
review's language label does not prove the local sentence contains a switch.
Several queries overlap, so their counts must not be added as unique passages.

| Report evidence | Origin and review key | Context |
| --- | --- | --- |
| Negation and contrasting evaluations | Collected `real:REV-06` | “not too spicy” and soup taste described as not “kaw” |
| English insertion in Malay preparation advice | Collected `real:REAL-004` | “Tak perlu goreng just rebus atau celur mi” |
| Informal abbreviations | Collected `real:REV-03`, `real:REAL-002` | Each contains one “mmg” and one “sgt” |

Each exported match retains its original text, source URL, origin, review ID, language label, sentence index, text hash and token offsets. Offsets are zero-based positions within a review, with an exclusive end; they are not original-text character positions. Exact kuah and kenyal occur in both collected and synthetic reviews.

## Bilingual reading aid

The 12 entries in `config/concordance_lexicon.csv` include sedap (tasty), pedas
(spicy), kuah (broth/gravy), kenyal (springy/chewy), tak (informal negation),
tapi (but), sgt (sangat), mmg (memang), kaw (context-sensitive concentrated/strong),
sedap gila (very tasty), not too spicy, and springy. This is a project-authored
lexicon, not a validated language-identification resource. The generated
evidence table supplies counts and all review keys; its KWIC companion permits
checking each occurrence. Single-occurrence forms such as kaw and sedap gila
are examples rather than established recurrent patterns.

## Reliability and remaining work

Automated checks verify unique `(origin, review_id)` identities, original hashes,
agreement of sentence/flat tokens, exact phrase matching, boundaries, overlaps,
negation preservation, zero hits and empty input. The exported manifest binds
the run to input hashes and selection parameters. Human interpretation uses
the full originals; no automated token language or sentiment labels are added.

The sentence splitter can oversplit abbreviations. Normalized token contexts
omit punctuation, case and emojis, which remain in originals. Inherited review
labels require group review, including ambiguous borrowing/brand mentions.
REV-01 retains its existing source/seasoning warning. The corpus is a convenience
sample across brands and contains substantial synthetic material; it does not
represent category-wide customer behaviour. Later Sheet edits require another
complete export and rerun of preprocessing, stop words, concordance and n-grams, with
the report evidence refreshed at the same time. Abstract and synthesis
sections of the report remain in progress.

## Reference

[1] S. Bird, E. Klein, and E. Loper, *Natural Language Processing with Python*,
O'Reilly Media, 2009, ch. 1, sec. 1.3, “Searching Text.”
https://www.nltk.org/book/ch01.html#searching-text (accessed 2026-11-09).
