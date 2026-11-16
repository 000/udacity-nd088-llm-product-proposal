# Proposed deployment and configuration

LineGuide revision 2.3.0, 16 November 2026. This is an unimplemented pilot design. No endpoint call, model benchmark, load test or provider-contract acceptance was performed.

## Model evidence and selection

Current Microsoft and OpenAI pages document `gpt-6-astra`, contradicting the supplied assessment's claim that the model is nonexistent. Microsoft identifies Azure version `2026-09-03`; OpenAI documents the direct alias `gpt-6-astra` [R01, R12, R13]. The Azure version must not be described as a direct OpenAI snapshot identifier. The [model verification record](../evidence/model-verification.json) separates these facts from untested application choices.

Retain Astra as a reference candidate for evaluation. It has not been selected through a LineGuide benchmark. Compare it with smaller eligible models on the same frozen tasks, measuring quality, latency and full operating cost. The current lifecycle evidence marks GPT-4.1 deprecated, the latest listed GPT-4o version Legacy, and the listed o1/o3/o4-mini alternatives near retirement [R14]. Check actual subscription eligibility before using any alternative. No Astra retirement date was found in the reviewed schedule; no date or unlimited availability is inferred.

## Proposed request

| Property | Proposed value | Reason and release condition |
| --- | --- | --- |
| Deployment | Azure OpenAI cloud deployment in a customer-approved geography and deployment type | Confirm model/version availability, lifecycle, quota and processing terms before provisioning. The scenario's 150 queries/day does not establish throughput or an optimal hosting choice. |
| Model identity | Azure model `gpt-6-astra`, version `2026-09-03`; the request's `model` field uses the actual Azure deployment name | R01/R12 document the interface. The deployment name and account access remain unassigned and unverified. |
| Sampling | `temperature: 0.1`; omit a `top_p` override | Limit sampling variation for grounded explanations. This does not guarantee determinism or accuracy [R02]. Stop and review any rejected configuration. |
| Reasoning | `reasoning: {"effort": "low"}` | A proposed latency/cost tradeoff supported by the documented model interface [R01, R13]. Evaluate the quality effect before pilot use. |
| Total input | At most 8,000 tokens across instructions, query, selected configuration, passages and request metadata | Enforce the application cap before generation. Preserve source warnings and applicability; clarify or escalate if evidence cannot fit. |
| Output | `max_output_tokens: 2000`, including reasoning; visible answer target at most 800 tokens | Keep answers brief. Reject incomplete or unvalidated output and return abstention or escalation. The visible target is not a separate vendor-enforced limit. |
| Deadline | 15 seconds from acceptance; validated-response p95 target at most 8 seconds | Count failures and timeouts against the latency gate. Both values are unmeasured requirements. |
| Behavior | Structured citations and clarification/escalation; no autonomous tool loop | Verify source applicability and exact permitted parts before display. The model has no controller route or credentials. |

The documented vendor ceilings exceed the proposed application budget, but do not establish runtime feasibility. The configuration must pass endpoint acceptance, quality, latency, incomplete-output and cost tests using the chosen deployment. No vendor price is used as an Azure quote, and the planning allowance remains an assumption.

## Grounding and optimization

Use classic RAG for approved, revisioned manuals and a separate authoritative relational catalogue for exact parts. Start with approximately 500-token sections, 80-token overlap, hybrid top 20 and reranking to at most five passages. These are initial settings for evaluation [R03, R04, R05, R10].

Changing manuals and compatibility records need revision and withdrawal without retraining. Keep those facts in governed records; weight fine-tuning is outside the pilot scope. Retrieval and citations still require applicability and correctness review.

## Proposed application data handling

| Data | Handling requirement |
| --- | --- |
| Model requests | Set `store: false`. Avoid Conversations and `previous_response_id`. Send required context explicitly for each request [R12]. |
| Application context | Keep query and answer context for the request lifetime only. Persist no chat history; disable raw-query and raw-answer logs. |
| Answer cache | Disable it for the first pilot. Any later cache requires tenant/permission isolation, revision invalidation and reviewed retention. |
| Audit metadata | Keep pseudonymous request ID, version IDs, policy outcome, timings and review disposition for a proposed 30 days. Delete expired records within the following 24 hours and verify applicable retained copies. Exclude raw prompts, answers, direct identity and secrets. |
| Customer content | Admit no proprietary customer data until privacy/security review accepts deployment type, provider terms, application controls and deletion behavior. |

Provider-managed processing and retention remain separate. `store: false` does not establish zero retention. Customer-specific abuse monitoring, geography and contract acceptance are unverified [R06, R12].

## Nodes, links and access

Require TLS 1.2 or later, using TLS 1.3 where supported. Use managed identities, least-privilege RBAC and private endpoints where each selected service supports them. An unavailable required control blocks release pending design review. Require AES-256 at rest for application stores, role-limited audit/catalogue access and reviewed key, backup and deletion behavior.

Derive tenant and entitlements from server-verified identity. Apply them before retrieval and again before delivery. Keep catalogue access read only. Isolation, revocation, injection and failure-path tests remain implementation work. Provider geography and storage behavior require checks against the actual deployment [R05, R06].

All references use the [source register](sources.json). Source existence and supported interfaces close a documentation question; operational suitability and industrial safety remain unverified.
