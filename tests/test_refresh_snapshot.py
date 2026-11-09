"""Check complete-corpus import without contributor, ID-prefix or language filters."""
import copy
import csv
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.refresh_snapshot import prepare_snapshot


def fixture():
    return {"spreadsheet_id": "1BzvT_kU5uHniEZFE2YcY6KccbnY7EIFWFnN0ebUUVvs",
            "snapshot_date": "2026-11-09", "sheets": [
        {"title": "Self-Collected Data", "range": "'Self-Collected Data'!A4:L1000",
         "values": [["Review ID", "Review Text", "Language Classification", "Notes"],
                    ["REV-01", "Original, text\nsecond line", "English", "unchanged"],
                    [], ["REAL-045", "sedap", "Malay"],
                    ["NEW-200", "good tapi mahal", "Code-switched"],
                    ["", "Missing ID is still audited", "Other/uncertain"]]},
        {"title": "AI-Generated Data", "range": "'AI-Generated Data'!A4:M1000",
         "values": [["Review ID", "Generated Review Text", "Language Classification", "Prompt"],
                    ["REV-AI-001", "AI original", "English"],
                    ["SYN-001", "AI addition", "Malay"],
                    ["", "", "", "prompt only"]]}]}


class SnapshotTests(unittest.TestCase):
    def test_all_ids_languages_and_source_rows_preserved(self):
        export = fixture()
        before = copy.deepcopy(export)
        outputs, manifest = prepare_snapshot(export)
        rows = list(csv.DictReader(io.StringIO(outputs["real_reviews.csv"])))
        self.assertEqual([r["Review ID"] for r in rows], ["REV-01", "REAL-045", "NEW-200", ""])
        self.assertEqual([r["source_row"] for r in rows], ["5", "7", "8", "9"])
        self.assertEqual(rows[0]["Review Text"], "Original, text\nsecond line")
        self.assertEqual(rows[0]["Notes"], "unchanged")
        self.assertEqual(manifest["review_counts"], {"real": 4, "ai": 2})
        self.assertEqual(manifest["omitted_nonreview_rows_in_export"], {"real": 1, "ai": 1})
        self.assertEqual(export, before)

    def test_no_fixed_row_limit(self):
        export = fixture()
        export["sheets"][0]["values"] = [export["sheets"][0]["values"][0]] + [
            [f"ANY-{i}", f"Review {i}", "English"] for i in range(300)]
        _, manifest = prepare_snapshot(export)
        self.assertEqual(manifest["review_counts"]["real"], 300)

    def test_invalid_source_and_incomplete_schema_fail(self):
        for mutate in [lambda x: x.update(spreadsheet_id="different"),
                       lambda x: x["sheets"].pop(),
                       lambda x: x["sheets"][0].update(range="A1:L1000"),
                       lambda x: x["sheets"][0]["values"][0].__setitem__(1, "Missing")]:
            export = fixture()
            mutate(export)
            with self.assertRaises(ValueError):
                prepare_snapshot(export)


if __name__ == "__main__":
    unittest.main()
