# Revision issue disposition

LineGuide revision 2.1.0, 16 November 2026. The baseline is commit `1e36e112faf02a1bf113c9015b70b0b178953c7d` and its preserved `v2-package`. [baseline-audit.json](../evidence/baseline-audit.json) records the input audit-bundle hash, actual baseline artifact hashes and agent findings. The supplied Gemini assessment was an evidentiary hold and checklist, with no completed slide-grading verdict.

This revision supersedes the baseline as the current review candidate. Prior decks, source files and evidence remain history. Their assertions of universal gate closure and human verification do not govern the current revision. At preparation, final export/visual review, complete manifests and publication were still pending; the table distinguishes changes in source from completed release verification.

## Findings and changes

| Baseline finding | Change in revision 2.1.0 | Disposition and limit |
| --- | --- | --- |
| C2-C3: Problem, scenario ledger and adoption details were largely in notes; no clear definition block. | Slide 2 names the business problem and current keyword-search/manual/catalog/support workflow. Slide 3 contains a labelled two-sentence definition. Slide 4 pairs features, benefits and friction. Slide 21 exposes every Scenario C constant, including overlapping education/device shares. | Addressed in source. Missing baseline performance and untested user benefits remain explicit; no substitute measurements are invented. |
| C4: Alternative comparison omitted explicit edge-case, maintenance and determinism dimensions. | Slide 5 compares keyword search, rules/intent trees and LLM/RAG across those dimensions and language flexibility. | Addressed in source. Comparative value still requires matched tasks. |
| C5: Bias/common-sense risks and enforceable cost controls were not explicit. | Slide 14 retains exactly five owned risks, adds novice/common-sense and language/user-bias review, and specifies token, concurrency and budget controls. Its notes distinguish a proposed allowance from a quotation and require reservation/reconciliation of delayed charges. | Addressed as a design requirement. Alerts alone do not enforce a hard ceiling; controls and fallback behavior remain unimplemented. |
| C7-C8: Incomplete ingestion, return/fallback paths, inconsistent component names and incomplete boundary/storage controls. | Slides 9-10 separate runtime and offline flows, using [canonical names](components.json). They show validation, response return, support, audit, indexing and revocation. Slides 11/13 and [CONFIGURATION.md](CONFIGURATION.md) describe capacity, outages, transport, at-rest protection and retention. | Addressed in design source. Diagram legibility must be checked after export. No deployed network, tested tenancy or deletion behavior is inferred. |
| C9: Contradictory Luna sampling support, deterministic-output wording, no explicit stateless request setting or concrete application retention. | Slide 12 proposes a documented Astra candidate and temperature 0.1 without a determinism guarantee. All input fits an 8,000-token cap. `store=false`, no conversation state, request-only application context, disabled answer caching and proposed audit expiry are explicit. | Addressed in source and configuration. Actual endpoint behavior, quota, cost, processing geography and provider retention acceptance remain open. |
| P1: Unsupported human-origin reasoning and universal human-review claims. | Slides 1/24 and [ATTRIBUTION.md](ATTRIBUTION.md) disclose substantive AI reasoning/content/code contributions and the absence of demonstrated universal human review. | Documentation corrected for this revision. Human authorship, independent understanding and submission eligibility remain unresolved. No course-specific permission was provided. |
| P2: Stale repository evidence, nonexistent README paths, an invalid Mac checksum command and incomplete manifest scope. | The revision has a separate artifact/source/docs/evidence structure. Current instructions must point only to published files and use `shasum -a 256 -c SHA256SUMS`. A new full manifest and final commit/tree evidence are required for this revision. | Release verification pending at preparation. Historical v1/v2 command output and hashes are preserved as dated evidence; they are not current default-branch proof. |
| P3: Missing assignment-linked HBR reference. | R11 appears in the source register and reference slide 23 with an explicit metadata/preview-only access limit. | Citation omission addressed. Full article access and body verification remain unavailable; no detailed article claim is relied upon. |
| Retained C6/C10 strengths: explicit goal hierarchy and five defined measurements. | Slide 7 retains one primary and two secondary goals. Slides 15-17 retain five KPIs, denominators, proposed thresholds and the validation plan. | Retained as artifact/design coverage. All operational values remain unmeasured. |
| Retained scenario and binary evidence. | Slide 21 preserves accurate Scenario C givens. Baseline binaries and their hashes are recorded in the baseline audit. The new candidate requires its own binary checks. | Historical baseline integrity is established locally; it does not prove the revision export or publication. |

## Reconciled requirement coverage

[CHECKLIST.md](CHECKLIST.md) maps every C1-C10 requirement and earlier G1-G8 gate to exact revised slide numbers. C2-C5 and C7-C9 contain the principal source changes. C1 requires current publication evidence. C6/C10 are retained with clear proposed/unmeasured status. Source attribution, starter-template limits, scenario/target separation and substantive AI disclosure are mapped separately from technical coverage.

## Work that remains open

| Open requirement | Evidence needed to resolve it |
| --- | --- |
| Baseline performance and customer appeal | Approved customer tasks, measured search/resolution/escalation baseline, user research and matched comparisons. |
| Product quality, safety and capacity | Independent domain/safety review, frozen semantic tests, per-language/model evaluation, load/isolation/injection/revocation/deletion/outage tests and reviewed failure behavior. No such product tests were run in this artifact revision. |
| Deployment and commercial terms | Account/model access, supported service controls, processing geography, provider retention/privacy terms, customer source permission and current quotations. |
| Academic authorship and eligibility | Independent student work and understanding, applicable course permission or guidance, and a truthful own-work declaration where required. Agent reviews cannot supply these. |
| Classroom submission | Eligibility must be resolved before any required attestation; the classroom would then need an actual submission and confirmation. This workflow performs neither. |
| Final revision artifact and publication proof | Export and visual checks, full manifest verification, actual non-LFS binary sizes/hashes, default-branch commit/tree proof and remote byte verification. Pending at preparation. |

Documentation can expose a missing measurement or approval without completing it. The current candidate therefore makes no claim of a deployed product, demonstrated benefits, completed human review, industrial safety certification, academic clearance or classroom submission.
