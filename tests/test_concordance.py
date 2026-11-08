"""Run: python -m unittest discover -s tests -p test_concordance.py"""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.concordance import concordance, load_reviews, rank_terms, run_analysis, summarize


def review(sentences, identifier="R1", origin="real", language="Code-switched"):
    tokens = [t for s in sentences for t in s]
    original = " ".join(tokens)
    return dict(origin=origin, review_id=identifier, language=language,
                sentence_tokens_before=sentences, tokens_before=tokens,
                original_text=original, text_sha256=hashlib.sha256(original.encode()).hexdigest(),
                included=True)


class ConcordanceTests(unittest.TestCase):
    def test_boundaries_and_offsets(self):
        rows = [review([["not", "too", "spicy"], ["sedap", "gila"]]),
                review([["spicy"]], "R2")]
        hits = concordance(rows, ["spicy sedap", "gila spicy", "sedap"], window=5)
        self.assertEqual(len(hits), 1)
        self.assertEqual((hits[0]["token_start"], hits[0]["token_end"]), (3, 4))
        self.assertEqual(hits[0]["left_context"], "")
        self.assertEqual(hits[0]["right_context"], "gila")

    def test_exact_casefolded_phrase_not_substring(self):
        hits = concordance([review([["TASTE", "tastes", "not", "too", "spicy"]])],
                           ["taste", " TASTE ", "NOT TOO SPICY"], window=1)
        self.assertEqual([h["query"] for h in hits], ["not too spicy", "taste"])
        self.assertEqual(hits[0]["keyword"], "not too spicy")
        self.assertEqual(hits[0]["left_context"], "tastes")

    def test_overlap_and_origin_identity(self):
        rows = [review([["sedap", "sedap", "sedap"]]),
                review([["sedap", "sedap"]], origin="ai", language="Malay")]
        hits = concordance(rows, ["sedap sedap"])
        summary = summarize(rows, ["sedap sedap", "absent"], hits)
        self.assertEqual(summary[0]["occurrences"], 3)
        self.assertEqual(summary[0]["reviews_containing"], 2)
        self.assertEqual(summary[0]["code_switched_reviews"], 1)
        self.assertEqual(summary[1]["occurrences"], 0)

    def test_preserves_negation_and_informal_tokens(self):
        row = review([["don't", "tak", "sedap", "sgt", "panas2"]])
        row["tokens_after"] = ["sedap"]
        hit = concordance([row], ["sedap"])[0]
        self.assertEqual(hit["left_context"], "don't tak")
        self.assertEqual(hit["right_context"], "sgt panas2")
        self.assertEqual(hit["original_text"], row["original_text"])

    def test_empty_zero_window_and_validation(self):
        self.assertEqual(concordance([], ["x"]), [])
        self.assertEqual(summarize([], ["x"], [])[0]["per_1000_tokens"], 0)
        hit = concordance([review([["x", "y"]])], ["x"], window=0)[0]
        self.assertEqual(hit["right_context"], "")
        for window in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                concordance([], ["x"], window)
        with self.assertRaises(ValueError):
            concordance([], [""])

    def test_frequency_ties_exclusions_and_excluded_rows(self):
        rows = [review([["shin", "the", "sedap", "kuah"]])]
        excluded = review([["fake"]], "R2")
        excluded["included"] = False
        rows.append(excluded)
        self.assertEqual(rank_terms(rows, {"the"}, {"shin"}), ["kuah", "sedap"])
        self.assertEqual(concordance(rows, ["fake"]), [])

    def test_loader_detects_stale_and_corrupt_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "ai_preprocessed.jsonl").write_text("", encoding="utf-8")
            row = review([["sedap"]])
            def save(records):
                (path / "real_preprocessed.jsonl").write_text(
                    "\n".join(json.dumps(r) for r in records), encoding="utf-8")
            save([row])
            self.assertEqual(len(load_reviews(path)), 1)
            save([row, row])
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                load_reviews(path)
            row["tokens_before"] = ["different"]
            save([row])
            with self.assertRaisesRegex(ValueError, "inconsistent"):
                load_reviews(path)
            row["tokens_before"] = ["sedap"]
            row["original_text"] = "edited"
            save([row])
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                load_reviews(path)

    def test_export_roundtrip_and_determinism(self):
        import csv
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            processed = root / "data" / "processed"
            processed.mkdir(parents=True)
            (root / "config").mkdir()
            row = review([["not", "sedap", "sedap"]])
            (processed / "real_preprocessed.jsonl").write_text(json.dumps(row), encoding="utf-8")
            (processed / "ai_preprocessed.jsonl").write_text("", encoding="utf-8")
            (processed / "stopwords_used.csv").write_text("word\nnot\n", encoding="utf-8")
            (root / "config" / "concordance_lexicon.csv").write_text(
                "expression,language,gloss,interpretation\nsedap,Malay,tasty,Check context\n",
                encoding="utf-8")
            result = run_analysis(root, ["sedap", "absent"], top_n=1)
            files_before = {p.name: p.read_bytes() for p in result["output_dir"].iterdir()}
            run_analysis(root, ["sedap", "absent"], top_n=1)
            self.assertEqual(files_before, {p.name: p.read_bytes() for p in result["output_dir"].iterdir()})
            with (result["output_dir"] / "kwic.csv").open(encoding="utf-8-sig", newline="") as f:
                exported = list(csv.DictReader(f))
            self.assertEqual(len(exported), 2)
            self.assertEqual(exported[0]["original_text"], row["original_text"])
            self.assertEqual(result["lexicon"][0]["review_keys"], "real:R1")
            self.assertEqual(result["manifest"]["unfiltered_tokens"], 3)


if __name__ == "__main__":
    unittest.main()
