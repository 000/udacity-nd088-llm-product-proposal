# Stack and configuration

The product architecture is proposed. The authoring workflow below was used to create this submission. Those two stacks have different purposes.

## Proposed product

A responsive mobile web client calls an authenticated server API. The API validates Microsoft Entra identity, derives tenant entitlements and requires robot applicability metadata before retrieval. Azure AI Search performs classic hybrid retrieval over approved, versioned documents. A separate relational catalog supplies exact compatible part records. Azure OpenAI in Microsoft Foundry provides a bounded explanation; server checks run before display.

The model candidate is `gpt-6-luna`, version `2026-09-22`, through the Responses API, with `reasoning.effort: low`. Proposed limits are 8,000 retrieved-context tokens, `max_output_tokens: 2000` including reasoning, a visible answer target of at most 800 tokens, and a 15-second end-to-end deadline. An incomplete response produces an approved excerpt or escalation. These limits need workload testing; Microsoft recommends a larger initial reasoning/output reserve while learning a workload. The tight cap could cause frequent incomplete responses.

No temperature override is specified because the current Microsoft feature table and unsupported-parameters section conflict. Endpoint compatibility must be tested before overriding sampling. This contradiction is preserved in the source audit. A low temperature would not establish correctness.

Start with `text-embedding-3-small`, section-aware chunks near 500 tokens with 80-token overlap, 20 hybrid candidates, reranking and at most five passages. All are tuning assumptions. Confirm model lifecycle, region, quota, embedding support and data-processing terms during procurement. Classic RAG was chosen for control and simplicity; newer agentic retrieval adds no necessary capability for this pilot. No fine-tuning, robot-control channel or autonomous tool loop is proposed.

Private connections, least privilege, encrypted transport, server-enforced access filters and an approved regional or DataZone deployment are requirements to implement and test. Provider abuse monitoring and storage require contractual review. Zero retention and compliance are not asserted. See source IDs R01 to R06 and R10 in [the register](sources.json).

## Submission authoring

The existing Herdr-owned workspace was reused, with one coordinator and explicit file ownership for research, product planning and deck production. The reference stack package was read as historical evidence. Its Vite/React website architecture was not transplanted into this deck or treated as a production requirement. Current lane instructions and service state governed execution.

The deck uses the bundled `@oai/artifact-tool` 2.8.157 with editable native text, tables and an architecture diagram. The source builder records its runtime interface. Rendering uses the available local presentation/PDF tooling; actual versions and rendering results are recorded in the verification evidence. The verifier uses Python's standard library. No application framework, database or production model endpoint was deployed.

The builder requires an environment providing the matching Artifact Tool runtime. That bundled dependency is not claimed to be independently obtainable through a public package registry. The editable PPTX, PDF and content JSON remain inspectable without that authoring runtime. File integrity and arithmetic verification require only Python.

For a rebuild, make that runtime resolvable to `source/build-deck.mjs` and run it with Node. `SOFFICE_BINARY` and `PDFTOPPM_BINARY` select the renderer and preview utility. `PRESENTATIONS_SKILL_DIR` enables the bundled presentation validators; `RUNTIME_PYTHON` selects their interpreter. Set `LINEGUIDE_OUTPUT_DIR`, `LINEGUIDE_BUILD_DIR` and `LINEGUIDE_PREVIEW_DIR` to separate writable directories to preserve the published files. Rendering metadata and generated object identifiers may change between builds; byte-identical rebuilds are not asserted. The published hashes bind the reviewed exports.

Hermes Shield Scanner 0.8.2 matches current PyPI metadata checked on 16 November 2026. The existing installation was reused through its sandboxed advisory wrapper. No global reinstall, runtime enforcement tier, automatic hook or blocking check was added. A bounded Google Decisions call has its own synthetic input, scope hash and advisory receipt. Cursor Projects readiness and its prepared public handoff are recorded separately.
