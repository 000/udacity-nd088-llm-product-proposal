# Revision issue disposition — 2.2.0

LineGuide revision 2.2.0, 16 November 2026. The baseline is commit `27e953a` (revision 2.1.0). This disposition addresses the five residual items in the 16 November 2026 audit of `27e953a`. No item changes product design content; items 3 and 4 change deck text, item 5 changes the build toolchain, and items 1 and 2 remain open by nature or by repository-level scope.

| Audit residual item | Disposition in revision 2.2.0 | Status |
| --- | --- | --- |
| **1. Udacity Honor Code authorship gate** (substantive AI generation recorded in root README, ATTRIBUTION, slides 1 and 24) | Unchanged and non-delegable. This revision keeps the truthful disclosure and makes no own-work or eligibility attestation. Do not submit for Udacity credit without written course-level permission for disclosed agentic co-generation, or an independent student rewrite; until then the repository remains an unsubmitted study reference. | **OPEN — documented, not resolvable by an artifact** |
| **2. Legacy `submission/` routing and unannotated `v2-package/README_v2.md`** | Not changed inside this package (it is repository-level). Recommended ready-to-apply plan, in increasing order of disruption: (a) prepend a deprecation header to `v2-package/README_v2.md` stating that v2.0.0 is superseded by `revisions/v2.2.0/`, that its build paths are stale, and that its attribution paragraph is retracted by the v2.1.0+ record; (b) move `submission/*` (v1.0.0/v1.1.0 decks) and `v2-package/` under `archive/` and place the canonical v2.2.0 PDF/PPTX at `submission/LineGuide_Proposal.pdf` / `.pptx`; (c) repoint the root README opening sentence at the canonical path. Any of (a)-(c) preserves history via git. | **OPEN — plan recorded; apply at repository level** |
| **3. Slide 11 speaker-note stale cache phrase** ("Cache only within tenant and permission scope.") | Patched to "If caching is enabled after pilot revocation testing, cache only within tenant and permission scope." Now consistent with slides 8, 10, 11 and 14 (initial answer caching disabled; caching only after revocation testing). | **CLOSED** |
| **4. Slide 18 on-slide unit conversion and equality** | Statement now reads "970.2 sessions/month × (5 ÷ 60) hours/session × $40/hour = $3,234/month", making the hour-cancellation explicit and the equality exact rather than approximate. | **CLOSED** |
| **5. Proprietary build dependency and unchecked slides 9-10 geometry** | The deck is rebuilt from the preserved v2.1.0 layout data by `source/build-deck.py`, which uses only public tooling (python-pptx, reportlab, Poppler); no `@oai/artifact-tool` or private runtime is required. Slides 9 and 10 were optically inspected from the committed previews: node labels, boundary labels and connector labels ("OIDC / TLS", "Validated answer or abstention", "Blocked / missing evidence", "Revision, approval and deletion events") render without clipping. | **CLOSED** |

## Verification record for this disposition

- `source/patch-v220.py` asserts the exact v2.1.0 strings it replaces; the patch output is `source/deck-content.json` with `version: 2.2.0`.
- `source/verify.py` re-runs the v2.1.0 checks against the v2.2.0 artifacts: 24 slides, 24 speaker notes, 8 native tables, 13 canonical component names, 12 references, arithmetic recomputation, and complete SHA256SUMS manifest coverage.
- `evidence/build-verification.json` records hashes, sizes and check results for this build.

## What remains open (unchanged from v2.1.0)

Baseline performance and customer appeal evidence; product quality, safety and capacity tests; deployment and commercial terms; academic authorship and eligibility; classroom submission. Documentation can expose a missing measurement or approval without completing it; this revision makes no claim of a deployed product, demonstrated benefits, completed human review, industrial safety certification, academic clearance or classroom submission.
