# Proposed deployment and configuration

LineGuide revision 2.1.0, 16 November 2026. These settings describe an unimplemented pilot. No endpoint call, quality evaluation, load test or provider-contract acceptance was performed.

## Model request

| Property | Proposed value | Reason and release condition |
| --- | --- | --- |
| Deployment | Azure OpenAI cloud deployment, in a customer-approved geography and deployment type | Confirm model availability, quota and processing terms before provisioning. The scenario's 150 queries/day does not by itself establish capacity or an optimal hosting choice. |
| Model | `gpt-6-astra`, version `2026-09-03` | Microsoft documents the required interfaces [R01, R12]. Benchmark quality, cost and latency before selecting it for a pilot. |
| Sampling | `temperature: 0.1`; leave `top_p` at the vendor default | Limit sampling variation for grounded explanations. This does not guarantee determinism or accuracy [R02]. If the endpoint rejects the request, stop and review configuration; do not silently change parameters. |
| Reasoning | `reasoning.effort: low` | Proposed latency and token-cost tradeoff; test against the frozen quality and safety set. |
| Total input | At most 8,000 tokens across instructions, query, selected configuration, retrieved passages and request metadata | Enforce the limit before generation; preserve source warnings and applicability metadata. Clarify or escalate when the evidence cannot fit. |
| Output | `max_output_tokens: 2000`, including reasoning; visible answer target at most 800 tokens | Keep explanations brief. Reject incomplete or unvalidated output and return a reviewed fallback or escalation. |
| Deadline | 15 seconds from acceptance; proposed validated-response p95 target at most 8 seconds | Timeouts count as failures in latency measurement and trigger fallback. These thresholds have not been measured. |
| Response behavior | Structured citations and clarification/escalation; no autonomous tool loop | Validate source applicability and exact part records before display. The model has no controller route or control credentials. |

R01's model/version and parameter statements support the candidate interface, not industrial suitability. The v2 Luna sampling conflict prompted this change. No current model is claimed to be the best choice without evaluation. Source R02 replaces the earlier direct-Luna-pricing reference; the planning allowance remains an assumption, not an Astra or Azure quote.

## Grounding and optimization

Use classic RAG for approved, revisioned manuals and a separate authoritative relational catalogue for exact parts. Start with approximately 500-token sections, 80-token overlap, hybrid top 20 and reranking to at most five passages. These are starting assumptions. Test source coverage and relevance before changing them.

Choose RAG over weight fine-tuning for changing manuals, revisions and part compatibility so that records can be withdrawn or updated without retraining. Fine-tuning is outside the pilot scope. Neither retrieval nor a citation establishes correctness on its own. Reviewers must test applicability, unsupported claims and abstention behavior [R03, R04, R05, R10].

## Application data handling

| Data | Proposed handling |
| --- | --- |
| Model requests | Set `store: false`. Do not create Conversations or use `previous_response_id`. Send the required context explicitly for each request [R12]. |
| Application context | Retain query and answer context for the request lifetime only. Persist no chat history. Disable raw-query and raw-answer logging. |
| Answer cache | Disable the tenant-scoped answer cache for the first pilot. Any later cache requires tenant/permission isolation, revision invalidation and a reviewed retention policy. |
| Audit metadata | Retain pseudonymous request ID, version identifiers, policy outcome, timings and review disposition for a proposed 30 days. Delete expired records within the following 24 hours and verify deletion, including applicable retained copies. Store no raw prompt, answer, direct identity or secret in this log. |
| Customer content | Admit no proprietary customer data until privacy/security review accepts the deployment type, provider terms, application controls and deletion plan. |

Provider-managed retention is separate from these application rules. `store: false` does not establish zero retention. Customer-specific monitoring, processing geography and contractual acceptance remain unverified [R06, R12].

## Nodes, links and access

Require TLS 1.2 or later on transport, using TLS 1.3 where supported. Use managed identities, least-privilege RBAC and private endpoints where the selected service supports them. If a required private endpoint or authentication control is unavailable, block release until the design is reviewed. Encrypt application stores at rest with AES-256, restrict audit and catalogue access by role, and review key ownership and backup/deletion behavior before customer-data use.

Derive tenant and entitlements from server-verified identity. Apply those constraints before retrieval and recheck them before response delivery. The parts path is read only. Proposed security controls still require isolation, revocation, injection and failure-path tests. Provider geography and storage behavior must be checked for the actual deployment [R05, R06].

Source identifiers refer to the [source register](sources.json). All configuration choices, retention periods and release conditions above are proposed requirements.
