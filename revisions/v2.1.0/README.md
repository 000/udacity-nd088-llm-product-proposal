# LineGuide revision 2.1.0

This 24-slide review candidate addresses the supplied Gemini evidence checklist and the gaps found in the v2 files. The actual assessment supplied an evidentiary hold and review criteria, without grading the unread slides. The [baseline audit](evidence/baseline-audit.json) records the new file-based findings. The [checklist](docs/CHECKLIST.md) and [issue disposition](docs/ISSUE-DISPOSITION.md) explain the revision and its remaining limits.

Open the [PDF](artifact/LineGuide_Proposal_v2.1.0.pdf) or [editable PowerPoint](artifact/LineGuide_Proposal_v2.1.0.pptx). Native tables and diagrams remain editable. The PDF is exported from the final PPTX through LibreOffice, rather than independently laid out. [Previews](previews/) show that PDF's pages.

The deck adds a visible Scenario C ledger, a two-sentence definition, feature/benefit/friction pairs, a four-dimension alternatives comparison and separate runtime and ingestion diagrams. Canonical component names match the [register](docs/components.json). The [configuration](docs/CONFIGURATION.md) records concrete request, privacy, retention and cost controls, all as proposed requirements. Five risks and five proposed product measurements remain bounded and explicit.

## Files and verification

| Path | Purpose |
| --- | --- |
| `artifact/` | Final PDF and PPTX binaries |
| `source/deck-content.json` | Complete slide content, notes and editable diagram geometry |
| `source/build-deck.mjs` | Local Artifact Tool builder |
| `source/verify.py` | Standard-library artifact, consistency, arithmetic and manifest checks |
| `docs/` | Checklist, issue disposition, sources, configuration, metrics, components and attribution |
| `evidence/` | Scoped baseline and revision checks; no operational test result |
| `previews/` | Final PDF page renders |
| `SHA256SUMS` | Every package file except the manifest itself |

From the repository root:

```sh
python3 revisions/v2.1.0/source/verify.py
/bin/bash tools/extract-audit.sh
```

Or verify checksums from this package directory:

```sh
shasum -a 256 -c SHA256SUMS
```

The extractor includes every tracked repository deck, including preserved historical versions. Its labelled v2.1.0 section is the current review target. Stage new intended files before extracting an uncommitted revision, because discovery deliberately excludes untracked files.

## Rebuild

The builder requires Node.js with `@oai/artifact-tool`, followed by LibreOffice and Poppler for PDF conversion and previews. Supply the local modules directory through `LINEGUIDE_MODULES` if normal module resolution cannot find it. The source contains no account-specific runtime path.

```sh
node revisions/v2.1.0/source/build-deck.mjs
soffice --headless --convert-to pdf --outdir revisions/v2.1.0/artifact revisions/v2.1.0/artifact/LineGuide_Proposal_v2.1.0.pptx
pdftoppm -scale-to 1600 -png revisions/v2.1.0/artifact/LineGuide_Proposal_v2.1.0.pdf revisions/v2.1.0/previews/slide
```

A rebuild changes container metadata and can change rendering across tool/font versions. Byte-identical reproduction is not asserted. Regenerate the manifests after a reviewed rebuild. Verification does not perform network calls or model inference.

## Open conditions

The [attribution](docs/ATTRIBUTION.md) discloses substantive AI contribution and corrects unsupported claims in v2. Student authorship, independent understanding and academic eligibility remain unresolved; no classroom submission occurred. Model access, provider contracts, safety review, customer sources, baseline research and operational tests also remain open. HBR's assignment-linked reference is included with a metadata/preview-only access limit. No result or approval is invented to mark those conditions closed.
