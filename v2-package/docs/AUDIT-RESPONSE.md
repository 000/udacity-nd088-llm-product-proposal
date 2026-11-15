# Audit response — LineGuide v2 evidence package

**Date:** 16 November 2026
**Prepared by:** Kimi Work agent (automated verification), reviewed by the human owner
**Scope:** This document responds to the external evidentiary hold placed on the GitHub repository `000/udacity-nd088-llm-product-proposal` (Udacity ND088, Scenario C "LineGuide" product proposal). Every command below was executed in this session against the existing clone at `repo/clone` and the revised package at `LineGuide_v2/`. Raw outputs are captured programmatically into the fenced blocks below. Machine-readable results are recorded in `evidence/verification-v2.json`; package integrity is covered by `LineGuide_v2/SHA256SUMS`.

---

## 1. Repository verification (was UNVERIFIED → now VERIFIED)

All git commands run read-only inside the existing clone at `repo/clone`.

**Working tree and branch state (`git status -sb`):**

```
## main...origin/main
```

The clone is on `main`, tracking `origin/main`, with no uncommitted changes.

**Remotes (`git remote -v`):**

```
origin	https://github.com/000/udacity-nd088-llm-product-proposal (fetch)
origin	https://github.com/000/udacity-nd088-llm-product-proposal (push)
```

**Default branch of the remote (`git symbolic-ref refs/remotes/origin/HEAD`):**

```
refs/remotes/origin/main
```

**Recent history (`git log -n 3 --oneline --decorate`):**

```
2451171 (HEAD -> main, origin/main, origin/HEAD) Add LineGuide proposal deck with sources and verification evidence
a25094a Initial commit
```

**Tracked tree at HEAD (`git ls-tree -r --long HEAD | head -40`):**

```
100644 blob 21f019dedca898e5b5fa51ad5eb0b4ac999b9d81      50	.gitignore
100644 blob 01a540f672039b9662a93f8180bac62e446263c9    1941	README.md
100644 blob 100b5d9f7edf0936addd0d90c6c3eedeee15c123    2659	SHA256SUMS
100644 blob 7aa43a668ccf82fa3e5a440585da56372bf16bfc     849	docs/architecture.mmd
100644 blob 59b0147bea45b7c40889b17b96b28934acb21649    1569	docs/cursor-project-brief.md
100644 blob 76dea50271190e08ef7d2f0ca0ef96c0fcb30e71    2137	docs/evidence-scope.md
100644 blob fb442a4e419e34788f4af9699b160cbfd143f64a    6420	docs/metrics.json
100644 blob c3ea6596d09417a4cc77788acb4cbe5597f2df5d   19067	docs/product-plan.md
100644 blob 44f8cbb69d3c3d3b59b88838ce7574b21ee642e7    2561	docs/rubric-map.md
100644 blob b94b74c8c9bb7753b6a20b76a0c45f1dac137be9    8222	docs/sources.json
100644 blob 85dfa0f59d1975228effd842df32aa7d5ed7ea59    4562	docs/tech-stack.md
100644 blob 60f4f8b874d5d2704427a388914f5bef8361f835    4169	docs/workflow.md
100644 blob bc132634a63d98200ae208af53ffdc0af903f722     987	evidence/authoring-provenance.json
100644 blob 052fbcf44436df2d6eaa50e3c58611ac921a7e82    1513	evidence/decisions-request.json
100644 blob 6dc58ae26aa4c530df65b5d0a26d7002770832d6    1617	evidence/decisions-result.json
100644 blob d349a7a0031e65d55ce3578e728f6a3f14480019     216	evidence/decisions-scope.json
100644 blob 04e50c22a82dcb4e569ee5d31b418ec0543d2558    2838	evidence/deck-review-final.json
100644 blob 38e8dfb52c43d59619339f6a18219aa93f24c883   11118	evidence/deck-review-initial.json
100644 blob 1b633b09fb17cfa489857cdabbce398987f185bb    4684	evidence/deck-validation.json
100644 blob 9c248863a29df3bb099daf750b039d9804a96526    1168	evidence/hermes-advisory.json
100644 blob 8343925e310300d8b380a44bc3084d746a214763    1940	evidence/hermes-report.json
100644 blob caf1b44c664007520bb7cdb71b60665c4a10cf54    7558	evidence/independent-product-review.json
100644 blob 478d7d2860a3440dd74b2e26640fc8618cad4f2d   14209	evidence/source-audit.json
100644 blob dffbdebc5f371c0d99d9c3e292270d00ee9edbe9    1737	evidence/verification.json
100644 blob a3da94e7418fcce231ef41d8581d3b04cd7db049    2088	evidence/visual-review.json
100644 blob 682d114a71aebc491234c7ba05895207293a3939    9812	source/build-deck.mjs
100644 blob 36fa8ea5533e8295045984af8eb738a7c528f390   32880	source/deck-content.json
100644 blob 9b64e0a5f4c5396b8ef78fca35f4cc5a32cf58ba    6279	source/verify.py
100644 blob ec43eab88d762c26002b14035116924cda264a43  300749	submission/LineGuide_Proposal.pdf
100644 blob 95629366b1b4c55a0f1d1bd560b8b1f9ebf27550  104699	submission/LineGuide_Proposal.pptx
```

Both deck binaries — `submission/LineGuide_Proposal.pdf` (300,749 bytes) and `submission/LineGuide_Proposal.pptx` (104,699 bytes) — are committed directly on `main` as regular git blobs, on the tip commit that is also `origin/main` and `origin/HEAD`. No Git LFS pointer files exist anywhere in the tree.

**Checksum verification (`shasum -a 256 -c SHA256SUMS`), run from `repo/clone`:**

```
.gitignore: OK
README.md: OK
docs/architecture.mmd: OK
docs/cursor-project-brief.md: OK
docs/evidence-scope.md: OK
docs/metrics.json: OK
docs/product-plan.md: OK
docs/rubric-map.md: OK
docs/sources.json: OK
docs/tech-stack.md: OK
docs/workflow.md: OK
evidence/authoring-provenance.json: OK
evidence/decisions-request.json: OK
evidence/decisions-result.json: OK
evidence/decisions-scope.json: OK
evidence/deck-review-final.json: OK
evidence/deck-review-initial.json: OK
evidence/deck-validation.json: OK
evidence/hermes-advisory.json: OK
evidence/hermes-report.json: OK
evidence/independent-product-review.json: OK
evidence/source-audit.json: OK
evidence/verification.json: OK
evidence/visual-review.json: OK
source/build-deck.mjs: OK
source/deck-content.json: OK
source/verify.py: OK
submission/LineGuide_Proposal.pdf: OK
submission/LineGuide_Proposal.pptx: OK
```

All 29 files verify against the committed `SHA256SUMS`, including both deck binaries.

**Binary reality check (`head -c 100 submission/LineGuide_Proposal.pdf | cat -v | head -2`):**

```
%PDF-1.7
%M-CM-$M-CM-<M-CM-6M-CM-^_
```

The file begins with a real `%PDF-1.7` header followed by binary comment bytes — a genuine PDF document, not a Git LFS pointer (an LFS pointer would be a small text file starting with `version https://git-lfs...`). The PPTX is likewise a real 104,699-byte ZIP container, confirmed openable by python-pptx in Section 2.

**Live repository metadata (`curl -s https://api.github.com/repos/000/udacity-nd088-llm-product-proposal`, selected fields):**

```json
{
  "full_name": "000/udacity-nd088-llm-product-proposal",
  "visibility": "public",
  "default_branch": "main",
  "pushed_at": "2026-11-15T21:53:34Z"
}
```

**Conclusions (Section 1):**

- The repository is **public** on GitHub.
- The **default branch is `main`**; the local clone is clean and identical to `origin/main` (HEAD `245117135e51f4c3bc1faae5c24d0a9a4640b1a5`).
- The deck **PDF and PPTX are real, non-LFS binary blobs committed on `main`**, pushed 2026-11-15.
- **`SHA256SUMS` verifies every file** in the repository (29/29 OK).
- The binaries are real: a **300,749-byte PDF** (genuine `%PDF-1.7` header) and a **104,699-byte PPTX** — no LFS pointers.

---

## 2. Slide deck verification (was UNVERIFIED → now VERIFIED)

Verification of `repo/clone/submission/LineGuide_Proposal.pptx` with python-pptx and of `repo/clone/submission/LineGuide_Proposal.pdf` with pypdf.

**PPTX integrity (python-pptx):** every slide has non-empty speaker notes; native tables are present on slides **4, 5, 10, 13, 14 and 17** (the audit's expected set), plus slide 12 (the five-risk register) — seven table slides in total, which exceeds rather than contradicts the expected set.

```
slide_count: 20
 1 | tables=0 | notes=488 chars | Hypothetical Scenario C proposal • Product not deployed
 2 | tables=0 | notes=652 chars | Technicians struggle to find applicable answers
 3 | tables=0 | notes=700 chars | The product and its customer benefit
 4 | tables=1 | notes=1087 chars | Use an LLM where conversation helps
 5 | tables=1 | notes=1181 chars | Existing industrial copilots set the comparison
 6 | tables=0 | notes=568 chars | System goals and first-release scope
 7 | tables=0 | notes=678 chars | The technician’s path through the product
 8 | tables=0 | notes=2325 chars | RAG architecture and trust boundaries
 9 | tables=0 | notes=1964 chars | Approved content controls retrieval quality
10 | tables=1 | notes=1970 chars | LLM deployment and configuration
11 | tables=0 | notes=1856 chars | Security and privacy requirements
12 | tables=1 | notes=1008 chars | Five risks and accountable mitigations
13 | tables=1 | notes=821 chars | Success measures: customer outcomes
14 | tables=1 | notes=1251 chars | Success measures: quality and reliability
15 | tables=0 | notes=827 chars | Validation before supervised use
16 | tables=0 | notes=755 chars | Illustrative monthly capacity value
17 | tables=1 | notes=886 chars | Sensitivity and investment discipline
18 | tables=0 | notes=1175 chars | Twelve-week pilot and stakeholder decision
19 | tables=0 | notes=514 chars | Sources: system design and privacy
20 | tables=0 | notes=468 chars | Sources: market, safety and model inputs
all_notes_non_empty: True
```

The deck has exactly **20 slides**; the titles above are the first text line of each slide (the deck uses text-box headings rather than title placeholders).

**PDF structure (pypdf):** the v1 PDF has **20 pages**, one per slide. Visible text extracted from the gate pages:

```
pages: 20
===== PAGE 3 =====
The product and its customer benefit
Proposed benefit; faster or safer outcomes have not been demonstrated 03
LineGuide explains approved reference material, cites its 
exact revision and retrieves verified parts for the 
selected robot configuration.
It asks for missing model or firmware details and prepares a technician-reviewed support 
handoff when evidence is missing or a request is hazardous.
Technicians gain a short explanation and an openable source for their machine.
===== PAGE 6 =====
System goals and first-release scope
Proposed scope; document suitability and language performance are untested 06
Primary goal Supervised English pilot
Increase verified self-service resolution of 
eligible documentation and catalog 
questions.
Secondary goals
Reduce time to a verified answer.
Prevent unsupported or hazardous 
assistance.
Two models; up to 200 approved articles 
across five topics, subject to content audit.
Read-only explanations and catalog lookup.
Spanish follows its own validation; other 
languages remain staged.
===== PAGE 8 =====
RAG architecture and trust boundaries
Proposed architecture • External generation remains subject to approved regional/provider terms 08
Device / public edge Private application and data services
Mobile web app
Technician + model 
ID
Entra ID + API
AuthZ and risk policy
Hybrid retrieval
Tenant + model + 
revision
Azure OpenAI
Cited draft only
Validation
Citations + parts
Approved manuals
Blob + search index
Parts catalogue
API-only SQL lookup
Human support
Escalation via API
Exact catalog records
TLS
Back-end links use private endpoints and managed identities. The API returns validated answers to 
the app; robot controllers remain disconnected.
===== PAGE 10 =====
LLM deployment and configuration
Candidate version is documented; account access, quality, latency and configuration are untested 10
Setting Pilot proposal
Hosted candidate Azure OpenAI gpt-6-luna, 2026-09-22; benchmark before selection
Generation Responses API; reasoning low; max_output_tokens 2,000 including reasoning
Context and timing
Retrieved context ≤8,000 tokens; visible answer target ≤800; 15-second 
deadline
Sampling Vendor default; test endpoint compatibility before overriding
Behavior and tuning Structured citations + escalation; no fine-tuning or autonomous tool loop
```

These extractions confirm the gate content: page 3 is the 3-sentence solution summary plus customer benefit; page 6 carries the explicit primary goal ("Increase verified self-service resolution…") with two named secondary goals and first-release scope; page 8 is the RAG architecture diagram with trust boundaries and security-labelled connections; page 10 is the concrete LLM deployment/configuration table (hosted candidate Azure OpenAI gpt-6-luna 2026-09-22, Responses API, reasoning low, max_output_tokens 2,000, context ≤8,000 tokens / ≤800 visible / 15-second deadline, sampling, behavior and tuning).

**Visual inspection:** the PDF pages were rendered to images (`pdftoppm`, all 20 pages) and visually inspected for text overflow and diagram legibility. Pages 3, 6, 8 and 10 were examined individually in this session: no text overflow or clipping was observed; the slide 8 architecture diagram is legible with all nodes, connections and security labels readable; the slide 10 settings table renders with all rows and cell text intact.

---

## 3. Revision v2 verification

SHA-256 digests computed with `shasum -a 256` inside `LineGuide_v2/` on 16 November 2026:

```
dd57684a17426c1a75a0d42245a03e18dfc94e1c02fd874a0176088923741602  artifact/LineGuide_Proposal_v2.pdf
d222ab1bfde3ebc5015d888c8f3674b534b6a2d311da1b9d8c61a67f0502fbab  artifact/LineGuide_Proposal_v2.pptx
b8930eb47c1aa0dfe3c4c6fc8b5caaa7bd755b66aa1cbf23b04d04f99031dda8  source/deck-content.json
1d54977c0fe77c881de28707b9f560e358310e1bbab628ddb4551c7ab1b0be83  source/build-deck.py
371653c0f36d183fb0089e4139965e378c4e9a8285997cec64387ee791960385  source/patch-v2.py
```

File sizes: `artifact/LineGuide_Proposal_v2.pdf` **30,097 bytes**; `artifact/LineGuide_Proposal_v2.pptx` **102,121 bytes**; `source/deck-content.json` 34,846 bytes; `source/build-deck.py` 18,985 bytes; `source/patch-v2.py` 6,567 bytes.

The v2 PDF has **20 pages** (pypdf). The v2 PPTX passes the same integrity checks as v1: 20 slides, non-empty speaker notes on all 20, native tables on slides 4, 5, 10, 12, 13, 14 and 17 (full per-slide listing in `evidence/verification-v2.json`).

**Builder reproducibility:** `source/build-deck.py` was re-run in this session against `source/deck-content.json` with output directed to a scratch directory (`LINEGUIDE_OUT`). It reproduces both artifacts: the rebuilt PPTX is member-for-member **byte-identical** to `artifact/LineGuide_Proposal_v2.pptx` (every ZIP member equal; only container entry timestamps differ, which is why the top-level SHA-256 differs), and the rebuilt PDF is **byte-identical** to `artifact/LineGuide_Proposal_v2.pdf` except for the embedded reportlab creation timestamps and the trailer `/ID` derived from them (identical 30,097-byte size). The builder is a deterministic function of `deck-content.json`.

**Package integrity:** `LineGuide_v2/SHA256SUMS` covers the two artifacts, three source files, the v1 content snapshot and the two docs registers; `shasum -a 256 -c SHA256SUMS` run inside `LineGuide_v2/`:

```
artifact/LineGuide_Proposal_v2.pdf: OK
artifact/LineGuide_Proposal_v2.pptx: OK
source/deck-content.json: OK
source/build-deck.py: OK
source/patch-v2.py: OK
source/deck-content-v1.json: OK
docs/sources.json: OK
docs/metrics.json: OK
```

---

## 4. Udacity policy pages

To remain within the audit's permitted evidence-gathering channels, **support.udacity.com and udacity.com/legal were not fetched live in this session**; this response makes no claim about the current verbatim text of those pages. Instead, the submission documents compliance **structurally** in `docs/ATTRIBUTION.md`, which covers:

- **Original authorship** — the product reasoning and the architecture diagram are the author's own work; AI assistance was limited to copy-editing, build scripting, rendering and cross-checking.
- **Citation** — dedicated references slides (19–20), a source register with claim limits and access dates (`docs/sources.json`), and per-slide evidence-status lines.
- **Epistemic honesty** — every results-bearing slide is labeled "proposed / unmeasured"; no fabricated interviews, users or results.
- **AI disclosure** — the roles AI tools played are stated explicitly; no claim originates from unreviewed tool output.

The reviewer is invited to check the policy text verbatim against `docs/ATTRIBUTION.md` and the honor-code mapping in `docs/RUBRIC-GATES-G1-G8.md` (controls H1–H4).

---

## 5. Conclusion

- The evidentiary hold is lifted for **G1**: the repository is public, the default branch is `main`, the deck PDF and PPTX are real non-LFS binaries committed on `main`, `SHA256SUMS` verifies all 29 repository files, and the deck is a complete 20-slide PPTX/PDF pair with full speaker notes, native tables and confirmed gate content.
- Every other audit gate (G2–G8) is mapped to slide-level evidence, with its rejection trap recorded, in `docs/RUBRIC-GATES-G1-G8.md`: G2, G3 and G8 already met in v1 and re-confirmed; G4–G7 closed in the v2 rebuild.
- The v2 revision package is internally consistent: artifact hashes are recorded in `LineGuide_v2/SHA256SUMS` (all OK), the machine-readable verification record is `evidence/verification-v2.json`, and the builder deterministically reproduces both v2 artifacts from `source/deck-content.json`.
