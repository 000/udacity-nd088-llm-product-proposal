> **DEPRECATED — superseded by [`revisions/v2.2.0/`](../revisions/v2.2.0/README.md) (16 November 2026).** This v2.0.0 package is retained as historical evidence only. Its build paths (`previews-artifact/`, `deck-content-v2.json`, `dist/`) are stale, its manifest covers a superseded build, and its attribution paragraph claiming human verification of every claim is retracted by the truthful AI-contribution record in `revisions/v2.1.0/docs/ATTRIBUTION.md`, carried forward in `revisions/v2.2.0/docs/ATTRIBUTION.md`. Reviewers should use `revisions/v2.2.0/`.

---

# LineGuide v2 — Revised submission package

Status: hypothetical Udacity ND088 Scenario C proposal, revised 16 November 2026. No customer interviews, production deployment, model evaluation, pilot outcome or safety certification is claimed anywhere in this package.

## What v2 is

The v1 deck in the public repository was placed on evidentiary hold by an external audit (Gemini, 16 November 2026) that could not verify the submitted artifacts. The audit defined eight evidence gates (G1–G8) and four honor-code controls (H1–H4). The v2 package rebuilds the 20-slide deck from a single machine-readable source of truth and closes the identified wording and evidence gaps. See [docs/RUBRIC-GATES-G1-G8.md](docs/RUBRIC-GATES-G1-G8.md) for the gate-by-gate mapping, [docs/CHANGELOG_v2.md](docs/CHANGELOG_v2.md) for the versioned change record, and [docs/AUDIT-RESPONSE.md](docs/AUDIT-RESPONSE.md) for the response to the audit findings.

The cover of the v2 deck reads "Revised submission v2 • 16 November 2026". The cover notes record the revision rationale.

## Package map

| Path | Contents |
|---|---|
| `artifact/` | The review-target deck: `LineGuide_Proposal_v2.pptx` and `.pdf` (real binaries, not LFS pointers) |
| `source/` | `deck-content.json` (v2 source of truth; same data as `deck-content-v2.json`), `deck-content-v1.json` (preserved v1 content), `build-deck.py` (dual-backend builder), `patch-v2.py` (v1→v2 patch script), `verify.py` |
| `docs/` | `sources.json` (source register R01–R10 with claim limits), `metrics.json` (machine-readable KPI inputs), `RUBRIC-GATES-G1-G8.md`, `ATTRIBUTION.md`, `CHANGELOG_v2.md`, and the audit response |
| `previews-artifact/` | Per-slide PNG renders of the `artifact/` deck (20 slides) |
| `dist/`, `submission/` | Rebuild output copies; `previews/`, `previews-dist/` their renders. `dist/` is the default builder output. |
| `evidence/` | Reserved for verification records accompanying publication |

`source/build-deck.py` is a single layout engine with two backends — python-pptx for the editable PPTX and reportlab for the PDF — both drawing from identical coordinates, so the PDF is a faithful render of the same content rather than a re-export.

## Rebuild

The v2 content was produced by patching the preserved v1 content:

```sh
python3 source/patch-v2.py
```

The deck is rebuilt from `source/deck-content.json`:

```sh
LINEGUIDE_OUT=artifact python3 source/build-deck.py
```

Omitting `LINEGUIDE_OUT` writes to `dist/`. The builder emits overflow warnings during build; a clean build should produce none. `source/verify.py` performs standard-library checks on structure, references and arithmetic.

## Verify

Once `SHA256SUMS` is published alongside the artifacts, confirm integrity:

```sh
sha256 -c SHA256SUMS
```

Further checks a reviewer can perform:

- Open `artifact/LineGuide_Proposal_v2.pdf` and confirm the page count is 20, matching the slide count in `source/deck-content.json`.
- Open `artifact/LineGuide_Proposal_v2.pptx` and confirm every slide carries speaker notes; each note ends with an evidence-status line and a checked-source list.
- Confirm slides 19–20 are dedicated references slides with clickable URLs, and that the R01 entry records the resolved sampling decision while preserving the vendor-documentation caveat.
- Compare `previews-artifact/slide-08.png` against the architecture prose on slide 8: connection labels, dashed trust boundary and the audit-events node should match the notes.

## What this package does not claim

This is a hypothetical proposal built on a supplied scenario. All scenario figures (7,500 articles, 150 queries/day, 45,000 parts, 15 models, language and device data) are given context, not measured company data. All KPI thresholds, budgets, staffing, sampling and deployment settings are proposed targets. No product result has been measured; no source has been interviewed; no funding or production approval is asserted.

## Provenance and AI assistance

Original product reasoning, architecture judgments and risk framing are the author's. AI tools were used for copy-editing, layout and build scripting, rendering, and cross-checking; the human verified every claim, arithmetic result and citation. The full honor-code statement is in [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md). Source claim limits and access dates (16 November 2026) are recorded in [docs/sources.json](docs/sources.json).
