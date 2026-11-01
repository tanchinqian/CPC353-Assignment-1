"""Exercise the notebook's cleaning code with edge-case fixtures.
Run: python tests/check_preprocessing.py
"""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
notebook = json.loads((ROOT / "preprocessing.ipynb").read_text(encoding="utf-8"))
codes = ["".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"]


def execute(index, namespace):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(codes[index], f"notebook-fixture-cell-{index + 1}", "exec"), namespace)


with tempfile.TemporaryDirectory(prefix="preprocessing-test-", dir=ROOT) as temp:
    assert Path(temp).resolve().is_relative_to(ROOT.resolve())
    old_directory = Path.cwd()
    try:
        os.chdir(temp)
        ns = {}
        execute(0, ns)
        pd = ns["pd"]

        def real(identifier, text, source="https://example.org/review"):
            return {"source_row": "5", "Review ID": identifier, "Review Text": text,
                    "Language Classification": "Code-switched", "Source URL": source,
                    "Product / Eatery Name": "Shin Ramyun",
                    "Notes / Annotator Comments": ""}

        def ai(identifier, text):
            return {"source_row": "5", "Review ID": identifier,
                    "Generated Review Text": text, "Language Classification": "English",
                    "Product / Eatery Name": "Shin Ramyun"}

        ns["tables"] = {
            "real": pd.DataFrame([
                real("R1", "Sedap!"), real("R2", "  SEDAP! "),
                real("X", "First conflicting ID"), real("X", "Second conflicting ID"),
                real("", "Missing ID"), real("E", "  "),
                real("M", "Good noodles", source=""),
                real("D", "Contains duck seasoning"),
            ]),
            "ai": pd.DataFrame([
                ai("A1", "SEDAP!"), ai("A2", "Not bad, tak mahal. Bukan awful!"),
                ai("", ""),
            ]),
        }
        for index in range(2, 9):
            execute(index, ns)
        audit, cleaned = ns["audit"], ns["cleaned"]
        assert len(audit) == 10  # Prompt-only/blank template is not a review.
        assert ns["ignored_rows"] == {"real": 0, "ai": 1}
        assert set(cleaned["review_id"]) == {"R1", "M", "D", "A2"}
        excluded = audit.loc[~audit["included"]].set_index("review_id")
        assert excluded.loc["A1", "duplicate_of"] == "real:R1"
        assert excluded.loc["R2", "duplicate_of"] == "real:R1"
        assert all(excluded.loc["X", "exclusion_reason"].str.contains("Repeated ID"))
        assert "Missing" in excluded.loc["", "exclusion_reason"]
        assert "empty" in excluded.loc["E", "exclusion_reason"]
        flags = ns["manual_queue"].set_index("review_id")
        assert "source URL" in flags.loc["M", "review_flags"]
        assert "seasoning" in flags.loc["D", "review_flags"]
        tokens = cleaned.set_index("review_id").loc["A2", "tokens_after"]
        assert {"not", "tak", "bukan"}.issubset(tokens)
        assert cleaned.set_index("review_id").loc["A2", "original_text"] == "Not bad, tak mahal. Bukan awful!"
        assert cleaned.set_index("review_id").loc["A2", "sentence_tokens_before"] == [
            ["not", "bad", "tak", "mahal"], ["bukan", "awful"]]
        print("Passed: missing IDs/text, duplicate IDs/text, real/AI priority,")
        print("blank templates, source flags, negations and sentence boundaries.")
    finally:
        os.chdir(old_directory)
