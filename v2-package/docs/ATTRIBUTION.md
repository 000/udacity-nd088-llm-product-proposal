# Attribution and honor-code statement

Prepared for the LineGuide v2 revision package, 16 November 2026. This statement supports honor-code controls H1–H4 in [RUBRIC-GATES-G1-G8.md](RUBRIC-GATES-G1-G8.md).

## Authorship

The original product reasoning is the author's: the problem framing for Scenario C, the primary and secondary system goals, the pilot scope, the choice of classic RAG over agentic retrieval and over fine-tuning, the comparison of an LLM against rule-based AI, keyword search and traditional automation, the five-risk register and its accountable owners, the KPI definitions and proposed gates, and the investment-discipline conclusion that the base case alone does not justify committing the full pilot budget.

The architecture diagram on slide 8 was originally authored for this design. Its components, trust boundaries and connection-level security labels express this proposal's judgments; it was not copied from vendor material or a prior submission.

## AI assistance

AI tools were used in the following supporting roles:

- Copy-editing of slide text and speaker notes.
- Layout and build scripting: `source/build-deck.py` (dual-backend PPTX/PDF builder) and `source/patch-v2.py` (v1→v2 patch), both generated and then human-reviewed.
- Rendering of the deck to PDF and per-slide preview images.
- Cross-checking: arithmetic on the capacity-value and sensitivity worksheets, consistency between slide text, notes and the source register, and rubric coverage.

AI tools were not used to invent data, interviews, benchmarks or results. No claim in the deck originates from an unreviewed tool output.

## Human verification

The human author verified every externally checkable claim, every arithmetic result (for example 150 × 22 × 0.60 × 0.70 × 0.70 = 970.2 sessions; 970.2 × 5/60 × $40 = $3,234; $800 + 16 × $50 = $1,600; $3,234 − $1,600 = $1,634) and every citation against the cited page on 16 November 2026. The overlapping scenario device and education percentages were left uncombined, as the scenario requires.

## Data provenance

The business scenario, knowledgebase counts, query volume, part and model counts, languages, age range and device/education figures are supplied hypothetical context from the assignment. They are not findings from company records. All KPI thresholds, adoption and eligibility shares, time-savings assumptions, budgets, staffing, sampling settings and deployment settings are proposed targets. None has been measured. No customer interviews were conducted and no production outcomes exist.

## Sources

Sources R01–R10 are real public pages, each accessed 16 November 2026, each carrying a recorded claim limit in [docs/sources.json](sources.json). Where vendor documentation conflicts — notably Microsoft documentation on gpt-6-luna temperature support — the conflict is preserved on the record rather than resolved by assertion; v2 sets a concrete target (temperature 0.0) with a documented fallback to the vendor default if the endpoint rejects the override.
