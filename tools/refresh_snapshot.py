"""Import a complete read-only Google Sheets values export into pipeline CSVs.

Usage: python tools/refresh_snapshot.py path/to/export.json
Export shape: {spreadsheet_id, snapshot_date, sheets: [{title, range, values}]}.
Each values array must begin with the row-4 headings. Read through the current
grid's last row for both review tabs; API omission of trailing blank rows is OK.
This importer does not access or modify the live Sheet.
"""
import argparse
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TABS = [("Self-Collected Data", "real_reviews.csv", "Review Text", "real"),
        ("AI-Generated Data", "ai_reviews.csv", "Generated Review Text", "ai")]


def prepare_snapshot(export):
    """Preserve all review candidates; leave exclusions to preprocessing."""
    date.fromisoformat(export["snapshot_date"])
    if export["spreadsheet_id"] != "1BzvT_kU5uHniEZFE2YcY6KccbnY7EIFWFnN0ebUUVvs":
        raise ValueError("Expected the documented project source spreadsheet")
    sheets = export["sheets"]
    outputs, counts, ranges, omitted = {}, {}, {}, {}
    for title, filename, text_field, origin in TABS:
        matches = [s for s in sheets if s["title"] == title]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one export of {title}")
        sheet = matches[0]
        if not re.search(r"!A4:[A-Z]+[0-9]+$", sheet["range"]):
            raise ValueError(f"Export must start at A4: {title}")
        values = sheet["values"]
        headings = values[0]
        if (not all(isinstance(h, str) and h.strip() for h in headings)
                or len(set(headings)) != len(headings)
                or not {"Review ID", text_field, "Language Classification"}.issubset(headings)):
            raise ValueError(f"Missing or duplicate headings: {title}")
        if "source_row" in headings:
            raise ValueError("source_row is reserved for the source sheet row number")
        stream = io.StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["source_row", *headings])
        count, ignored = 0, 0
        for number, raw in enumerate(values[1:], start=5):
            if len(raw) > len(headings) and any(v not in (None, "") for v in raw[len(headings):]):
                raise ValueError(f"Unheaded data at {title} row {number}")
            row = ["" if value is None else str(value) for value in raw[:len(headings)]]
            row += [""] * (len(headings) - len(row))
            record = dict(zip(headings, row))
            if not record["Review ID"].strip() and not record[text_field].strip():
                ignored += 1
                continue
            writer.writerow([number, *row])
            count += 1
        outputs[filename] = stream.getvalue()
        counts[origin], omitted[origin] = count, ignored
        ranges[title] = sheet["range"]
    manifest = {
        "source_spreadsheet_id": export["spreadsheet_id"],
        "source_url": f'https://docs.google.com/spreadsheets/d/{export["spreadsheet_id"]}/edit',
        "snapshot_date": export["snapshot_date"],
        "method": "Complete read-only values export of both review tabs. All rows with an ID or review text retained for preprocessing; blank/template/prompt-only rows omitted. No contributor, product, date, origin or language selection.",
        "sheets": {filename: title for title, filename, _, _ in TABS},
        "read_ranges": ranges, "review_counts": counts,
        "omitted_nonreview_rows_in_export": omitted,
        "scope": "All review candidates from both source tabs; instant noodle products across brands.",
        "dates": "Preserved as supplied metadata. Assigned dates are not assumed to be verified publication dates; dates are not linguistic features.",
        "ai_provenance": "Generation and seed fields preserved per row; theme-based and seed-linked examples coexist. No provenance is inferred.",
        "input_sha256": {name: hashlib.sha256(value.encode("utf-8-sig")).hexdigest()
                         for name, value in outputs.items()},
    }
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()
    outputs, manifest = prepare_snapshot(json.loads(args.export.read_text(encoding="utf-8-sig")))
    destination = ROOT / "data" / "raw"
    for name, value in outputs.items():
        (destination / name).write_bytes(value.encode("utf-8-sig"))
    (destination / "source_snapshot.json").write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print("Review candidates exported:", manifest["review_counts"])
    print("Omitted non-review rows:", manifest["omitted_nonreview_rows_in_export"])


if __name__ == "__main__":
    main()
