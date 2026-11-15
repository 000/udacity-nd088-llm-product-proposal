# Response to the external assessment

Version 1.1.0, 16 November 2026. The attached Gemini assessment placed the repository on an evidence hold because its session had not retrieved the files. It did not establish a failed slide or a failed rubric row. This revision uses direct artifact inspection, current classroom and policy review, and a complete review bundle to address that evidence gap. It also corrects the focused design/documentation issues found through inspection.

## Tracked issues

| ID | Response and evidence | Disposition |
|---|---|---|
| LG-01 | Actual PDF/PPTX, README, complete manifests and source files are supplied in the review bundle. Baseline commit/tree, public/default-branch and non-LFS evidence are recorded. The final revision is identifiable through its committed files and version | Artifact-evidence gap addressed; an outside auditor must still open the supplied files |
| LG-02 | C1 to C10 have matching IDs and labels in both diagrams and the component register. Ingestion, exact catalog validation, validated return, support and audit flows are explicit, with connection protections and provider-processing qualifications | Addressed in slides 8, 9 and 22 and the component register |
| LG-03 | Total input is 12,000 tokens with explicit allocations; output reserve is 2,000 including reasoning. Capacity, overflow, incomplete-output and privacy behavior are documented. Temperature is explicitly not sent pending compatibility testing | Addressed in slides 11 and 23 and the configuration record; endpoint testing remains proposed pilot work |
| LG-04 | README and slide 25 disclose substantive AI-generated reasoning, architecture, prose, diagrams and code. Agent verification is distinguished from student authorship and understanding | Attribution gap addressed; no student-authorship certification made |
| LG-05 | Current official policy and the live classroom own-work affirmation were read. Artifact checks and disclosure cannot establish the learner's own assessed work | **OPEN: academic eligibility. No submission or success confirmation exists** |
| LG-06 | The classroom starter resource was identified, but bounded download attempts did not retrieve a verified file. The custom layout and generated diagrams use no starter template; no template-matching or exhaustive originality claim is made | Evidence boundary clarified; template retrieval remains unverified |
| LG-07 | Version 1.1.0 appears in the artifacts and metadata; new filenames and a change log distinguish the revision. Original exports, source archive and immutable baseline commit remain available | Versioned-delivery gap addressed |
| LG-08 | The existing five risk groups now visibly identify unequal-language-quality/bias and the unpriced operational cost of delay | Addressed in slide 13 without inventing a monetary benefit or adding ungrouped risks |

An additional inspection finding was corrected in slide 17: the visible economic equation now divides minutes by 60 before multiplying by hourly value. The numerical result and staged recommendation are unchanged.

The classroom's optional suggestions are also addressed. Slide 24 and the prompt document contain fictional System/User examples with an explicit missing-evidence expectation. The reference-data plan identifies type, amount, provenance, approval, bias checks and refresh/withdrawal behavior. These additions are not observed product tests.

## Reconciled gates

G1 concerns packaging and default-branch evidence. G2 to G8 concern scenario/problem, concise solution and alternatives, five risks, goal hierarchy, architecture/security, configuration and five success measurements. The [rubric map](rubric-map.md) links each gate to the revised slides and supporting records. Evidence of coverage does not constitute an Udacity grade or acceptance decision.

The four integrity controls retain separate conclusions. Scenario facts and proposed targets are distinguished. The diagram has recorded AI authoring provenance and the deck has no remaining starter-placeholder text; no exhaustive comparison with external student work was performed. External factual claims retain source attribution. AI provenance is now explicit. Student authorship and academic eligibility remain unresolved.

## Verification and remaining work

The baseline review checked all 30 retrieved file hashes, actual binary formats and Git objects, 20 slides/notes, six rendered samples and 21 independent arithmetic checks. Revised records describe the 25-slide artifacts, current source/diagram consistency, every-slide rendered review and a separate independent review. Earlier advisory scan and synthetic Decisions records describe v1.0.0 only.

The review bundle contains actual binaries and an independently usable manifest. `python3 source/verify.py` checks the extracted bundle or repository. A downloaded committed revision must match these bytes before publication is reported complete. The final publication receipt is retained locally and the committed GitHub history identifies the public revision; no self-referential commit hash is fabricated inside the artifacts.

The correct classroom project and repository route are verified. The own-work affirmations remain unchecked and Submit is disabled. The learner needs to complete the assessed analysis through their own permitted effort, or establish a specific applicable authorization from Udacity. Neither a cosmetic rewrite nor checking the box closes that gap. No message was sent to Udacity support.
