"""Reproducible sentence-bounded KWIC over the preprocessing JSONL exports.

Only the Python standard library is needed. Never use filtered tokens for KWIC.
Token offsets are zero-based within a review, end-exclusive; not character offsets.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


KWIC_FIELDS = [
    "query", "origin", "review_id", "language", "switching_type", "product",
    "sentence_index", "token_start", "token_end", "left_context", "keyword",
    "right_context", "sentence_text", "original_text", "text_sha256",
    "source_url", "review_flags",
]
SUMMARY_FIELDS = ["query", "occurrences", "reviews_containing", "per_1000_tokens",
                  "code_switched_occurrences", "code_switched_reviews"]


def load_reviews(processed_dir):
    """Reject corrupt/stale exports instead of silently changing the corpus."""
    rows, seen = [], set()
    for origin in ("real", "ai"):
        path = Path(processed_dir) / f"{origin}_preprocessed.jsonl"
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("included") is False:
                continue
            key = (row.get("origin"), row.get("review_id"))
            if key[0] != origin or not isinstance(key[1], str) or not key[1].strip():
                raise ValueError(f"Invalid review identity in {path.name}: {key}")
            if key in seen:
                raise ValueError(f"Duplicate origin/review_id: {key}")
            seen.add(key)
            sentences, tokens = row.get("sentence_tokens_before"), row.get("tokens_before")
            if (not isinstance(sentences, list) or not isinstance(tokens, list)
                    or not all(isinstance(s, list) and s for s in sentences)
                    or not all(isinstance(t, str) and t for t in tokens)
                    or [t for s in sentences for t in s] != tokens):
                raise ValueError(f"Missing or inconsistent unfiltered sentence tokens: {key}")
            original = row.get("original_text")
            if not isinstance(original, str) or not original.strip():
                raise ValueError(f"Missing original text: {key}")
            if hashlib.sha256(original.encode("utf-8")).hexdigest() != row.get("text_sha256"):
                raise ValueError(f"Original-text hash mismatch: {key}")
            rows.append(row)
    return sorted(rows, key=lambda r: (r["origin"], r["review_id"]))


def normalize_queries(queries):
    """Queries are whitespace-separated literal tokens, not regex or substrings."""
    result = []
    for query in queries:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Each query must be a non-empty token or token phrase")
        value = " ".join(query.casefold().split())
        if value not in result:
            result.append(value)
    return result


def concordance(rows, queries, window=5):
    if isinstance(window, bool) or not isinstance(window, int) or window < 0:
        raise ValueError("window must be a non-negative integer")
    queries = normalize_queries(queries)
    hits = []
    for row in rows:
        if row.get("included") is False:
            continue
        offset = 0
        for sentence_index, sentence in enumerate(row["sentence_tokens_before"]):
            folded = [token.casefold() for token in sentence]
            for query in queries:
                needle = query.split()
                for start in range(len(sentence) - len(needle) + 1):
                    end = start + len(needle)
                    if folded[start:end] != needle:
                        continue
                    hits.append({
                        "query": query,
                        **{field: row.get(field, "") for field in
                           ("origin", "review_id", "language", "switching_type", "product",
                            "original_text", "text_sha256", "review_flags")},
                        "sentence_index": sentence_index,
                        "token_start": offset + start, "token_end": offset + end,
                        "left_context": " ".join(sentence[max(0, start - window):start]),
                        "keyword": " ".join(sentence[start:end]),
                        "right_context": " ".join(sentence[end:end + window]),
                        "sentence_text": " ".join(sentence),
                        "source_url": row.get("Source URL", ""),
                    })
            offset += len(sentence)
    return sorted(hits, key=lambda h: (h["query"], h["origin"], h["review_id"], h["token_start"]))


def summarize(rows, queries, hits):
    total = sum(len(row["tokens_before"]) for row in rows if row.get("included") is not False)
    result = []
    for query in normalize_queries(queries):
        selected = [h for h in hits if h["query"] == query]
        switched = [h for h in selected if h["language"].casefold() == "code-switched"]
        result.append({
            "query": query, "occurrences": len(selected),
            "reviews_containing": len({(h["origin"], h["review_id"]) for h in selected}),
            "per_1000_tokens": round(len(selected) / total * 1000, 3) if total else 0,
            "code_switched_occurrences": len(switched),
            "code_switched_reviews": len({(h["origin"], h["review_id"]) for h in switched}),
        })
    return result


def rank_terms(rows, stopwords, excluded, top_n=12):
    """Rank candidates by combined-corpus frequency, breaking ties alphabetically."""
    if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n < 0:
        raise ValueError("top_n must be a non-negative integer")
    blocked = {word.casefold() for word in set(stopwords) | set(excluded)}
    counts = Counter(t.casefold() for r in rows if r.get("included") is not False
                     for t in r["tokens_before"] if t.casefold() not in blocked)
    return sorted(counts, key=lambda term: (-counts[term], term))[:top_n]


def write_csv(path, rows, fields):
    with Path(path).open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run_analysis(project_dir, queries, window=5, top_n=12, excluded=()):
    root = Path(project_dir)
    processed = root / "data" / "processed"
    rows = load_reviews(processed)
    with (processed / "stopwords_used.csv").open(encoding="utf-8-sig") as file:
        stopwords = {r["word"] for r in csv.DictReader(file)}
    candidates = rank_terms(rows, stopwords, excluded, top_n)
    queries = normalize_queries([*queries, *candidates])
    hits = concordance(rows, queries, window)
    summary = summarize(rows, queries, hits)
    output = root / "data" / "analysis" / "concordance"
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "kwic.csv", hits, KWIC_FIELDS)
    write_csv(output / "keyword_summary.csv", summary, SUMMARY_FIELDS)
    lexicon_path = root / "config" / "concordance_lexicon.csv"
    with lexicon_path.open(encoding="utf-8-sig") as file:
        lexicon = list(csv.DictReader(file))
    lexicon_fields = list(lexicon[0]) if lexicon else ["expression", "language", "gloss", "interpretation"]
    lexicon_hits = concordance(rows, [entry["expression"] for entry in lexicon], window)
    for entry in lexicon:
        evidence = [h for h in lexicon_hits if h["query"] == entry["expression"].casefold()]
        entry["occurrences"] = len(evidence)
        entry["review_keys"] = ";".join(sorted({f'{h["origin"]}:{h["review_id"]}' for h in evidence}))
    write_csv(output / "lexicon_evidence.csv", lexicon,
              lexicon_fields + ["occurrences", "review_keys"])
    write_csv(output / "lexicon_kwic.csv", lexicon_hits, KWIC_FIELDS)
    inputs = [processed / f"{origin}_preprocessed.jsonl" for origin in ("real", "ai")]
    inputs += [processed / "stopwords_used.csv", lexicon_path]
    manifest = {
        "review_count": len(rows), "origin_counts": dict(sorted(Counter(r["origin"] for r in rows).items())),
        "language_counts": dict(sorted(Counter(r["language"] for r in rows).items())),
        "unfiltered_tokens": sum(len(r["tokens_before"]) for r in rows),
        "queries": queries, "window_tokens_each_side": window, "top_n": top_n,
        "frequency_candidates": candidates, "candidate_exclusions": sorted(excluded),
        "context_boundary": "sentence", "matching": "casefolded exact token sequence; overlapping hits retained",
        "token_offsets": "zero-based review token start; exclusive end",
        "input_sha256": {str(p.relative_to(root)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "interpretation": "Review language labels are inherited, not token-level switch detection. Check original text.",
    }
    (output / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"reviews": rows, "hits": hits, "summary": summary, "lexicon": lexicon,
            "manifest": manifest, "output_dir": output}
