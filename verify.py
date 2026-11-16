#!/usr/bin/env python3
"""Run the sole current candidate verifier from any working directory."""
from pathlib import Path
import json,runpy
root=Path(__file__).resolve().parent
current=json.loads((root/'CURRENT.json').read_text())
target=(root/current['candidate_path']/'source/verify.py').resolve()
assert target.is_relative_to(root) and target.is_file()
runpy.run_path(str(target),run_name='__main__')
