# LineGuide revision 2.2.0

This 24-slide review candidate applies the residual polish ledger from the 16 November 2026 audit of commit `27e953a` (v2.1.0). It changes no design content, metric, KPI, or disclosure: the two deck-level corrections are the slide 11 speaker-note caching condition and the slide 18 dimensional equation. See [docs/ISSUE-DISPOSITION-v2.2.0.md](docs/ISSUE-DISPOSITION-v2.2.0.md) for the item-by-item record.

Open the [PDF](artifact/LineGuide_Proposal_v2.2.0.pdf) or [editable PowerPoint](artifact/LineGuide_Proposal_v2.2.0.pptx). The deck is rebuilt from the preserved v2.1.0 layout data with a public-tooling builder (python-pptx + reportlab), so external auditors can now regenerate both artifacts without the proprietary `@oai/artifact-tool` runtime. [Previews](previews/) show the rendered PDF pages, including optically inspected slides 9, 10, 11 and 18.

## Files and verification

| Path | Purpose |
| --- | --- |
| `artifact/` | Final PDF and PPTX binaries |
| `source/deck-content.json` | Complete slide content, notes and diagram geometry (v2.2.0) |
| `source/deck-content-v2.1.0.json` | Preserved v2.1.0 source this revision patches |
| `source/patch-v220.py` | Standard-library patch generating v2.2.0 content from the preserved source |
| `source/build-deck.py` | Public-tooling dual-backend builder (PPTX via python-pptx, PDF via reportlab) |
| `source/verify.py` | Standard-library artifact, consistency, arithmetic and manifest checks |
| `docs/` | Attribution, issue disposition, checklist, configuration, components, sources |
| `evidence/` | Build verification record and carried v2.1.0 evidence |
| `previews/` | Rendered PDF pages |
| `SHA256SUMS` | Every package file except the manifest itself |

After this package is committed, from the repository root:

```sh
python3 revisions/v2.2.0/source/verify.py
```

Or verify checksums from this package directory:

```sh
shasum -a 256 -c SHA256SUMS
```

## Rebuild

Requires Python 3 with `python-pptx` and `reportlab`, plus Poppler for previews. No proprietary module, account path, or network access is needed.

```sh
python3 revisions/v2.2.0/source/patch-v220.py   # regenerates deck-content.json from the preserved v2.1.0 source
LINEGUIDE_OUT=revisions/v2.2.0/artifact python3 revisions/v2.2.0/source/build-deck.py
pdftoppm -scale-to 1600 -png revisions/v2.2.0/artifact/LineGuide_Proposal_v2.2.0.pdf revisions/v2.2.0/previews/slide
```

A rebuild changes container metadata and can change rendering across tool or font versions; byte-identical reproduction is not asserted. Regenerate the manifest after a reviewed rebuild.

## Open conditions

The [attribution](docs/ATTRIBUTION.md) discloses substantive AI contribution. Student authorship, independent understanding and academic eligibility remain unresolved; no classroom submission occurred and no own-work attestation is made. Model access, provider contracts, safety review, customer sources, baseline research and operational tests also remain open. The v2.1.0 open-conditions record governs everything not explicitly changed by this revision.
