"""Execute this project's plain-Python notebook cells without a Jupyter install.

Run from anywhere: python tools/run_notebook.py [notebook.ipynb]
The saved notebook contains actual stdout/stderr from each executed code cell.
Select preprocessing.ipynb, stopword_analysis.ipynb or concordance_analysis.ipynb. For interactive work,
open the selected notebook in Colab or Jupyter instead.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import traceback
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_NOTEBOOKS = {"preprocessing.ipynb", "stopword_analysis.ipynb", "concordance_analysis.ipynb"}
NOTEBOOK_NAME = Path(sys.argv[1]).name if len(sys.argv) > 1 else "preprocessing.ipynb"
if NOTEBOOK_NAME not in ALLOWED_NOTEBOOKS:
    raise SystemExit(f"Choose one of: {', '.join(sorted(ALLOWED_NOTEBOOKS))}")
NOTEBOOK = ROOT / NOTEBOOK_NAME


def run():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    execution = 0
    previous_directory = Path.cwd()
    try:
        os.chdir(ROOT)
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            execution += 1
            cell["execution_count"] = execution
            stdout, stderr = io.StringIO(), io.StringIO()
            try:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    exec(compile("".join(cell["source"]),
                                 f"{NOTEBOOK_NAME}:cell-{execution}", "exec"), namespace)
            except Exception:
                cell["outputs"] = [{"output_type": "stream", "name": "stderr",
                                    "text": traceback.format_exc().splitlines(True)}]
                NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
                                    encoding="utf-8")
                raise
            cell["outputs"] = [
                {"output_type": "stream", "name": name, "text": stream.getvalue().splitlines(True)}
                for name, stream in [("stdout", stdout), ("stderr", stderr)] if stream.getvalue()
            ]
            print(f"Executed code cell {execution}")
        NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")
        print("Notebook executed successfully; outputs saved.")
    finally:
        os.chdir(previous_directory)
    return namespace


if __name__ == "__main__":
    run()
