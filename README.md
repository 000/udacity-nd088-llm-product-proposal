# LineGuide v1.1.0

A hypothetical industrial robot expert advisor proposal for Udacity ND088, Scenario C. Revised 16 November 2026.

Open the [revised PDF](submission/LineGuide_Proposal_v1.1.0.pdf), download the [editable PowerPoint](submission/LineGuide_Proposal_v1.1.0.pptx), or use the [complete review bundle](submission/LineGuide_v1.1.0_review_bundle.zip). These files are on the repository's default branch, `main`.

> **Audit-ready candidate — v2.0.0 supersedes v1.1.0.** The folder [`v2-package/`](v2-package/README_v2.md) holds the revised submission package prepared against the 16 November 2026 evidentiary audit: a rebuilt 20-slide deck, a gate-by-gate compliance matrix (G1-G8 and honor-code controls, independently audited as passing), the audit-response evidence with captured verification output, an attribution statement, and a SHA256SUMS manifest. Start at `v2-package/README_v2.md`. The academic-eligibility caution in this README applies equally to v2.0.0; no eligibility or own-work attestation is made, and v2.0.0 has not been submitted in the classroom.

Academic eligibility remains open. Codex generated substantial product reasoning, architecture choices, calculations, prose, diagrams, slide content and verification code. Agent reviews and artifact checks do not establish student authorship or independent understanding. The current [Udacity Honor Code](https://www.udacity.com/en-US/legal/honor-code) restricts substantial AI production of assessed work; disclosure alone does not authorize it. This revision has not been submitted in the classroom and makes no own-work or eligibility attestation.

LineGuide would help authorized technicians find approved documentation and compatible catalog records. Its architecture has no robot-control connection. Scenario figures, planning assumptions and proposed release targets are identified separately. No customer interviews, production service, model evaluation, pilot results or industrial safety certification is claimed.

The [revision response](docs/revision-response-v1.1.0.md) accounts for every assessment issue and retains the unresolved academic-eligibility item. The [rubric map](docs/rubric-map.md), [component register](docs/component-register.md), [configuration](docs/proposed-model-config.json), [reference-data plan](docs/reference-data-plan.md), [sample prompts](docs/prompt-examples.md) and [product plan](docs/product-plan.md) provide the detailed reasoning. The [source register](docs/sources.json) and [revision evidence](evidence/v1.1.0/) support review.

Verify the downloaded repository or extracted review bundle from its root:

```sh
python3 source/verify.py
```

The verifier checks all manifest entries, binary headers, PPTX structure and notes, component/configuration consistency, and illustrative economics. It tests artifact integrity, not an operational advisor. The review bundle has its own complete manifest and includes the actual files for an auditor who cannot retrieve GitHub URLs. Rebuilding the deck requires the [documented authoring runtime](docs/tech-stack.md); byte-identical rendering is not asserted.

The original [v1.0.0 PDF](submission/LineGuide_Proposal.pdf) and [PowerPoint](submission/LineGuide_Proposal.pptx) remain unchanged. Its complete publication is preserved at [commit 2451171](https://github.com/000/udacity-nd088-llm-product-proposal/tree/245117135e51f4c3bc1faae5c24d0a9a4640b1a5), with its original authoring files also retained in [the archive](archive/v1.0.0/). Earlier evidence at the root of `evidence/` describes that baseline; dated revision evidence describes v1.1.0.
