#!/usr/bin/env python3
"""Generate deck-content.json (v2.2.0) from the preserved v2.1.0 source.

Applies only the residual polish ledger from the 16 Nov 2026 audit of 27e953a:
  item 3 - Slide 11 notes: cache sentence aligned with the disabled-caching design
  item 4 - Slide 18: dimensional exact equation with explicit (5 / 60) hours conversion
Plus version markers. No design, metric, KPI or provenance content changes.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
c = json.loads((HERE / "deck-content-v2.1.0.json").read_text())

c["version"] = "2.2.0"
c["date"] = "2026-11-16"

cover = c["slides"][0]
cover["meta"] = "Scenario C, Udacity ND088\nRevision 2.2.0, 16 November 2026"
cover["notes"] += (" Revision 2.2.0 applies the residual polish ledger from the 16 November 2026 audit of "
                   "commit 27e953a: slide 11 speaker-note caching wording and slide 18 dimensional notation. "
                   "No design content, metric, or disclosure changes. AI-contribution and eligibility records stand.")

s11 = c["slides"][10]
assert s11["title"] == "Retrieval, validation and capacity limits"
old = "Cache only within tenant and permission scope."
assert old in s11["notes"]
s11["notes"] = s11["notes"].replace(
    old,
    "If caching is enabled after pilot revocation testing, cache only within tenant and permission scope.")

s18 = c["slides"][17]
assert s18["title"] == "Illustrative monthly capacity value"
s18["statement"] = "970.2 sessions/month × (5 ÷ 60) hours/session × $40/hour = $3,234/month"
s18["notes"] += (" The on-slide equation now shows the exact unit conversion: (5 / 60) hours per session "
                 "cancels against $/hour, making the equality 970.2 × (5 / 60) × 40 = 3,234 dimensionally explicit.")

s24 = c["slides"][23]
assert s24["title"] == "Provenance and review status"
s24["notes"] += (" Revision 2.2.0 records two documentation-level polish items (slide 11 note wording; slide 18 "
                 "exact equation) and no other change. Repository-hygiene recommendations from the same audit "
                 "(legacy submission/ routing; v2-package deprecation header) are addressed in "
                 "revisions/v2.2.0/docs/ISSUE-DISPOSITION-v2.2.0.md.")

(HERE / "deck-content.json").write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n")
print("wrote deck-content.json version 2.2.0, slides:", len(c["slides"]))
