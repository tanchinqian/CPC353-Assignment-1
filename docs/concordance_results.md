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
preprocessed JSONL files generated from refreshed raw CSV snapshots. All three
implemented notebooks were rerun together; the live source Sheet was read only.
Shared report and resource URLs are in `PROJECT_CONTEXT.md`.

## Method

Concordance places a selected word or phrase beside its surrounding text so
that its use can be interpreted in context [1]. This implementation searches
case-folded exact token sequences in unfiltered sentence arrays. It displays
up to five tokens on each side, clips at sentence boundaries and retains all
overlapping matches. It never joins reviews or constructs phrases across
sentences. Every hit carries its origin, review ID, language label, source URL,
original text/hash, sentence index and review-token offsets.

Selection combines 32 explicit English/Malay attribute, evaluation, negation
and contrast queries with the top 12 token types after excluding project stop
words and six listed product-name tokens. Deduplication yields 37 queries and
332 query-occurrence records (overlapping queries are not unique passages).
Frequency ties are resolved alphabetically. The selected frequency candidates
are noodles, but, mi, kuah, sedap, flavour, rasa, tak, kari, kuahnya, noodle,
and spicy. Stop words remain in context; their exclusion affects candidate ranking
only. Variant forms remain separate: kuah does not include kuahnya, and spicy
does not include spiciness. The curated selection is not an exhaustive attribute
dictionary. Occurrence counts, distinct review coverage and frequencies per
1,000 unfiltered tokens are exported, including zero-hit queries.

## Evidence from the combined corpus

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

### Context examples and interpretation

- **Collected real:REV-06:** `springy texture of the noodles [not too spicy] but the soup taste is`.
  The complete review contrasts an acceptable heat level with soup described
  as not “kaw”. This shows why the negator and contrast marker must remain:
  the isolated keyword spicy would lose the degree qualification. “Kaw” is
  context-sensitive colloquial Malaysian usage; the example is not automatic
  proof of a particular lexical language or switching category.
- **Synthetic ai:REV-AI-001:** `kuah shin ramyun memang [pedas] but the springy noodles make`.
  A Malay clause about heat is followed by an English clause about texture,
  joined by “but”. This illustrates an intra-sentential shift and a trade-off
  between attributes. Because it is AI-generated, it is evidence of the
  constructed corpus rather than independent customer behaviour.
- **Synthetic ai:REV-AI-034:** `shin ramyun ni [sedap gila] bila mi masih firm dan`.
  The Malay intensifier phrase occurs beside the English adjective “firm”.
  This illustrates lexical insertion into the surrounding Malay wording;
  it does not establish which pattern is most common in real reviews.
- **Synthetic ai:REV-AI-035:** the full original has a Malay sentence describing
  heat and taste, followed by “The noodles also held their shape well.” This
  illustrates an inter-sentential shift. Sentence-clipped KWIC deliberately
  keeps the two sentences separate; the exported original permits inspection.
- **Collected real:REAL-004 (Mi Sedaap Sambal Goreng):** “Tak perlu goreng just
  rebus atau celur mi” places English “just” within Malay preparation advice.
  This is a collected example from the additional rows now included in the
  full corpus. It concerns preparation convenience, not just taste or texture.
- **Collected real:REV-03 and real:REAL-002:** “mmg” and “sgt” each occur twice
  across these two reviews. They are preserved as informal spellings rather
  than silently expanded. Glosses are interpretation aids; the searched
  evidence remains the original tokens.

The examples support contextual discussion of taste/heat, broth, texture and
preparation convenience.
They do not establish customer sentiment, rank all attributes, or estimate
language-switch rates. Exact kuah and kenyal now occur in both collected and
synthetic reviews; source keys in the evidence files keep that distinction
visible. Combined-corpus frequency is not a measure of independent customer
preference.

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
complete export and rerun of preprocessing, stop words and concordance, with
the report evidence refreshed at the same time. N-gram, abstract and synthesis
sections remain unfinished.

## Reference

[1] S. Bird, E. Klein, and E. Loper, *Natural Language Processing with Python*,
O'Reilly Media, 2009, ch. 1, sec. 1.3, “Searching Text.”
https://www.nltk.org/book/ch01.html#searching-text (accessed 2026-11-09).
