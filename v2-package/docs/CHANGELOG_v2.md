# Changelog — LineGuide v2

All changes were produced by `source/patch-v2.py` applied to the preserved v1 content (`source/deck-content-v1.json`), then rendered by `source/build-deck.py`. Every entry is tagged with the audit gate (G1–G8) or honor-code control (H1–H4) it addresses. Dates: 16 November 2026.

## v1.0.0 → v2.0.0

### Added

- **Single source of truth and dual-backend builder.** The v2 deck is built from `source/deck-content.json` by `source/build-deck.py`, one layout engine with two backends (python-pptx for PPTX, reportlab for PDF) drawing from identical coordinates, so the PDF is a faithful render of the same content. The patch from v1 is reproducible via `source/patch-v2.py`. [G1]
- **Revision marker.** Cover meta now reads "Revised submission v2 • 16 November 2026"; cover notes record the revision rationale and point to README_v2 and docs. [G1, H3]
- **Connection-level security on the architecture slide.** Slide 8 adds per-connection labels ("TLS 1.3 + authenticated session", "private endpoint, approved region", "read-only SQL"), a dashed trust boundary with its own label, a new "Audit events / Pseudonymous, filtered" node reached by a dashed arrow, and an updated summary sentence matching the speaker-note prose. [G6]
- **Concrete LLM configuration.** Slide 10 replaces the generic settings row with six concrete rows — deployment model (cloud on Azure, approved region or DataZone, private endpoints, managed identities; no on-prem/edge node at 150 queries/day), hosted candidate (Azure OpenAI gpt-6-luna, version 2026-09-22), generation (Responses API, reasoning low, max_output_tokens 2,000 including reasoning), context budget (system prompt + retrieval ≤8,000 tokens, visible answer ≤800, 15-second deadline), sampling (temperature 0.0 target with documented fallback to vendor default if the endpoint rejects the override), and behavior (structured citations + escalation; no fine-tuning or autonomous tool loop). Speaker notes justify each setting. [G7]
- **On-slide opportunity-cost statement.** Slide 12 gains a caption: "Delay risk: continued search friction and escalation; monetary size unknown — bounded discovery limits exposure." [G4]
- **Evidence status in every slide's notes.** Each speaker-note block now ends with an evidence-status line and a checked-source list, making the evidence trail auditable slide by slide. [H2, H3]
- **Documentation package.** New `README_v2.md`, `docs/RUBRIC-GATES-G1-G8.md`, `docs/ATTRIBUTION.md` and this changelog. [G1, H1–H4]

### Changed

- **Slide 6 title and headings.** Retitled "System attributes: goals and pilot scope"; the left heading now reads "Primary system goal" above the single primary goal, with the two secondary goals explicitly labeled beneath. [G5]
- **R01 source register entry and slide 19 notes.** Updated to record the resolved sampling decision — a concrete temperature target of 0.0 with a fallback to the vendor default recorded at deployment — while preserving the vendor-documentation caveat that Luna temperature compatibility remains unresolved between Microsoft's feature table and unsupported-parameters section. [G7, H3]
- **Slide 10 sampling row.** Same resolution as R01: target 0.0, fallback documented, residual variance controlled by deterministic guardrails (entitlement filtering, exact catalog matching, citation validation, abstention). [G7]

### Unchanged, and why

- **G2 (Scenario anchor):** Slides 1–2 already named Scenario C, stated the problem, the current workaround and its flaws, and gave demographics with overlapping figures flagged. Re-verified against the audit wording; no change required.
- **G3 (Solution):** Slide 3 already gave a 1–3 sentence solution summary with benefits and necessary features; slide 4 already argued why an LLM beats rule-based AI, keyword search and traditional automation. Re-verified; no change required.
- **G8 (Success metrics):** Slides 13–14 already carried five user-centered KPIs with exact definitions, denominators, sample sizes and proposed gates. Re-verified; no change required.
- **Economics slides 16–17:** The capacity-value and sensitivity worksheets were already labeled illustrative with inspectable arithmetic; re-verified, arithmetic unchanged.
- **V1 deck in the repository:** remains the originally submitted artifact; v2 is staged alongside it, not merged over it.

## Verification checklist

- [ ] `python3 source/patch-v2.py` regenerates `deck-content-v2.json` identical to `source/deck-content.json`.
- [ ] `LINEGUIDE_OUT=artifact python3 source/build-deck.py` completes with no overflow warnings.
- [ ] `artifact/LineGuide_Proposal_v2.pdf` has exactly 20 pages.
- [ ] All 20 slides in `artifact/LineGuide_Proposal_v2.pptx` carry speaker notes ending in an evidence-status line and checked-source list.
- [ ] Slide 8 diagram labels match the speaker-note prose (connection labels, trust boundary, audit-events node).
- [ ] Slide 10 six configuration rows match `docs/sources.json` claim limits for R01, R02, R10.
- [ ] Slides 19–20 URLs are clickable and resolve to the R01–R10 pages.
- [ ] `sha256 -c SHA256SUMS` passes once the checksum file is published.
- [ ] Every results-bearing slide footer still reads proposed/unmeasured; no measured result has entered the deck.
