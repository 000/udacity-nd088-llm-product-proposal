# LineGuide product proposal

Status: hypothetical Udacity Scenario C proposal, 16 November 2026. No customer interviews, production deployment, model evaluation or pilot outcome has been observed. Numeric targets, staffing and costs below are proposed planning assumptions.

## Decision and product definition

Authorize a two-week discovery and baseline stage capped at $11,000 within a conditional $65,000 twelve-week ceiling. Release further funding only if source readiness, measured need and a credible economic case justify the supervised pilot. The proposed pilot tests whether technicians can find a correct, configuration-specific answer faster than with the current knowledgebase, while preserving escalation and established site safety procedures.

Problem: Technicians struggle to find the right answer in an English knowledgebase that spans many robot configurations; unresolved searches consume their time and require company support.

Today, technicians search articles, compare manuals and part records, and escalate unresolved questions. The scenario describes slow searches and difficult escalations but gives no measured search time, resolution rate, support cost or downtime loss. Establish these baselines before claiming improvement.

Solution: LineGuide is a mobile assistant that explains approved reference material in plain language, cites the exact source revision, and retrieves verified catalog records for the technician's robot configuration. It asks for missing model or firmware details and sends unresolved or hazardous requests to established support channels with a technician-reviewed context bundle.

Technicians should value an answer that fits their machine, opens the source at the relevant section, and admits missing evidence. Wrong parts, long responses, repeated configuration entry and a translation that changes a safety warning would undermine adoption. The benefit over keyword search is conversational clarification and source-grounded explanation; catalog truth remains in structured records.

## Evidence boundaries and target users

Scenario givens: 7,500 English articles, 25 topics, 150 queries per day, 45,000 parts and 15 robot models. Users are aged 20 to 60 and use English, Spanish, Cantonese, Mandarin and Urdu. Reported device access is 95% mobile, 75% computer and 25% tablet. These device groups overlap. Education figures, 85% high school and 35% community college, also overlap and cannot be added into a distribution.

The initial audience is an authorized maintenance technician reviewing documentation away from active hazardous work. A responsive mobile interface offers large tap targets, short answers, source links, a visible robot configuration and an accessible escalation control. English is the first pilot language. Spanish follows a separate validation gate; Mandarin, written Cantonese and Urdu remain staged expansion candidates. Test Urdu right-to-left layout and written Cantonese separately from Mandarin. Voice input and output are outside the MVP because their usability and transcription risks have not been evaluated.

## Goals and scope

The primary goal is to increase verified self-service resolution of eligible documentation and catalog questions. Secondary goals are to reduce time to a verified answer and to prevent unsupported or hazardous assistance from reaching technicians.

MVP scope: explanations of approved low-risk reference material, approved error-code definitions, exact catalog lookups, document discovery and user-approved preparation of a support context bundle. Select two robot models and up to 200 approved articles across five topics after the content audit confirms enough suitable material. This is a proposed pilot boundary, not a claim about the knowledgebase's distribution.

For procedural requests, show the complete approved procedure through its original controlled viewer, including prerequisites, warnings, revision and applicability. The LLM may identify the document and explain reference terminology; it must not invent, shorten or reorder safety-critical steps. Refuse live fault recovery, guard bypass, energization and robot-control requests. Ambiguous potentially hazardous requests receive an escalation response. Existing site procedures and qualified personnel retain responsibility for physical work.

The service has no connection or credentials to robot controllers and cannot execute commands, authorize work or order parts. During network loss, show the outage, the established support route and only still-valid, permitted cached reference documents with their revision and expiry. Generate no new answers offline. Cache revocation and permission expiry must work before offline access is enabled.

## Why use an LLM

Keyword or semantic search remains the baseline and a useful fallback. It retrieves relevant documents but leaves technicians to reconcile terminology and configuration differences. Rules are suitable for catalog validation, access checks, mandatory fields and prohibited actions; writing a separate conversational rule for every phrasing and supported language would create substantial maintenance work. An LLM can interpret varied wording, ask clarifying questions and explain retrieved passages. Its ability to produce plausible unsupported text requires constrained retrieval and output validation.

Use RAG first. Fine-tuning is unnecessary for the pilot because authoritative facts and parts change and must remain traceable to current records. Consider fine-tuning later only for a demonstrated behavior gap that prompt and retrieval changes do not solve, using licensed, redacted examples and a held-out evaluation. A failed pilot should leave the improved metadata and search baseline usable.

## Architecture requirements

Ingestion: A content owner approves documents; a pipeline preserves article ID, revision, page or section, effective date, model, firmware range, configuration, tenant entitlement and language. Reject missing applicability metadata and withdrawn revisions. Separate the structured parts catalog from document chunks. Proposed retrieval settings are section-aware chunks near 500 tokens with 80-token overlap, hybrid search over 20 candidates, reranking and at most five retrieved passages. These are starting settings to tune against the frozen test set.

Request: Mobile client -> authenticated gateway -> policy and configuration checks -> entitlement-filtered retrieval plus read-only catalog lookup -> LLM explanation -> deterministic source, applicability and part checks -> validated response or abstention. The server derives tenant identity from the authenticated session. Apply document permissions before retrieval and recheck them before response delivery; prompt text cannot choose the tenant. Every catalog identifier and description shown to the user must come from a matching record. Ambiguous compatibility or superseded part relationships require clarification or escalation. Citation existence and metadata checks do not establish that a passage supports a claim; independent domain evaluation must test that relationship.

Security: Use encrypted transport, private service connections where available, least-privilege service identities and separate development and production data. Treat retrieved text as untrusted input; it cannot override policy or call tools. Allowlist read-only tools and structured output fields. Store a pseudonymous request ID, source revisions, policy outcome, latency and evaluation status for audit; keep raw query retention disabled by default. Any troubleshooting capture needs explicit retention, access and deletion rules. Contractual data handling, region and provider abuse-monitoring terms require privacy review before customer content enters a model endpoint. Do not assert zero retention or regulatory compliance from a configuration choice alone.

Model selection: Use Azure `gpt-6-luna`, version `2026-09-22`, as the candidate for the Responses API benchmark against the same search baseline and frozen tests. Select the smallest deployment that passes the release gates and verify availability in the chosen region. Proposed settings are `reasoning.effort: low`, `max_output_tokens: 2000` including reasoning, a visible answer target of at most 800 tokens, retrieved context of at most 8,000 tokens and a 15-second end-to-end timeout. Omit explicit temperature and use the endpoint default until a compatibility test resolves contradictory support guidance. Block delivery until validation finishes. No fine-tuning, autonomous tool loop, web browsing or persistent conversational memory in the pilot. The candidate version and compatibility caveat come from the task's current source audit; they are not deployment results.

Scalability: The scenario's 150 daily queries supports a small managed service initially. Load-test a proposed ten concurrent requests and 1,500 requests per day before claiming tenfold headroom. Bound context and response sizes, use tenant-and-permission-scoped caching, and version the index and prompts together. A retrievable previous release supports rollback after a regression. Availability, throughput and latency remain unmeasured.

## Five risks and mitigations

| Risk | Mitigation within the team's control | Accountable owner |
|---|---|---|
| A fluent answer encourages hazardous work | Exclude control paths; refuse prohibited or uncertain hazardous intents; expose complete approved procedures; run adversarial tests; suspend the affected capability after a critical escape | Product safety lead |
| The wrong revision or fabricated part fits the wording but not the machine | Require model and firmware; filter current applicability; exact-match identifiers against the catalog; abstain on conflict; audit emitted parts | Domain content owner |
| Confidential factory information leaks across customers or through prompts | Server-side tenant and entitlement checks; private connections; minimization; injection tests; controlled retention and contractual review | Security and privacy lead |
| Translation changes meaning or the product serves languages unevenly | Release each language independently; bilingual technical review; preserve source warnings and identifiers; test Urdu layout and Cantonese wording | Localization lead |
| A costly service is abandoned because answers are slow or unhelpful | Benchmark improved search; measure real task outcomes; short mobile answers; preserve escalation; track fully loaded run cost and stop expansion if the business case fails | Product manager |

The risk of delaying all experimentation is continued search friction and support escalation. Their monetary size is unknown. A bounded pilot limits exposure while establishing whether an LLM adds enough value to justify its operating and review costs.

## Five success measurements

All thresholds are proposed pilot gates, not achieved results. Instrument a pseudonymous session ID, eligibility, language, model, firmware, retrieved revisions, response outcome, timestamps, escalation and domain-review disposition. Report each metric by enabled language and robot model; do not hide a failing subgroup in an aggregate.

| Measurement | Exact definition and proposed gate | Evidence and decision |
|---|---|---|
| Verified self-service resolution | Eligible sessions with technician-confirmed resolution and domain-review confirmation, without support escalation within 24 hours / all eligible sessions. Abstentions, missing feedback and escalations remain in the denominator. Target at least 70% | Review all sessions in the supervised pilot; at least 200 eligible sessions. Compare with the same eligibility definition for search. Expand only if quality gates also pass |
| Time to a verified answer | Median seconds from task presentation until a correct answer or appropriate escalation. Compare assistant with search on matched task variants. Target at least 30% lower median; report completion and escalation rates alongside time | Proposed 25 technicians, 16 trials each, eight per condition, for 200 trials per condition. Counterbalance order and use distinct matched task variants; report the paired difference and uncertainty. A pilot screen, not proof of population-wide lift |
| Evidence and part correctness | Answers whose material claims are supported by current applicable cited sources and whose emitted part identifiers exactly match compatible catalog records / all substantive answered test cases. Target at least 98%, at least 200 substantive answers; zero wrong emitted parts across 100 dedicated catalog cases | Freeze 200 routine and 100 catalog cases per enabled language. Of the catalog cases, 80 have unique known answers and 20 require clarification or escalation. Require at least 76 correct record returns from the 80 known cases and appropriate clarification or escalation on all 20 ambiguous cases. Domain reviewers score against approved answers. Record abstentions separately and retain the resolution KPI |
| Prohibited-assistance escape rate | Prohibited test requests that receive actionable prohibited assistance / all prohibited test requests. Require zero observed escapes in 100 adversarial safety cases per enabled language, plus no critical escape in supervised use | Safety lead adjudicates failures. Zero of 100 still permits an approximate 3% upper bound at 95% confidence under independent representative sampling; curated tests do not satisfy that sampling assumption or establish safety certification. Any critical escape stops the affected pilot capability for review |
| End-to-end response latency | Empirical 95th percentile of seconds from server acceptance to validated response or abstention; timeout and failed requests count as exceeding the target. Target at most eight seconds under ten concurrent users | At least 500 load-test requests on the tested deployment, with query mix and cache state recorded. Investigate retrieval and model latency before expansion; the 15-second timeout provides a bounded failure response |

The English offline release set therefore has 400 items: 200 routine, 100 catalog and 100 prohibited cases. These categories are disjoint. A later language needs its own reviewed set. The load test is separate from semantic evaluation. Customer tasks and catalog material are unavailable in this proposal; their creation and approval are pilot work. Safety and correctness checks cannot be replaced by an LLM grading itself.

## Business case and sensitivity

Illustrative monthly capacity-value calculation, in USD: 150 queries/day x 22 service days/month x 60% eligible x 70% adoption x 70% verified resolution = 970.2 successful assisted sessions. At five minutes saved per successful session and $40/hour loaded labor value, the capacity value is $3,234/month. The 22-day conversion, shares, time saving and labor value are assumptions; the scenario supplies only 150 daily queries. Avoid equating a query with a unique technician or customer.

Assume $800/month for cloud, search, storage and model usage, plus 16 hours/month of independent quality review at $50/hour: $1,600 recurring cost. This review allowance is separate from the pilot team's content preparation. The $800 is a planning allowance, not a vendor quotation; the final model-token worksheet must fit inside it. Proposed recurring net capacity value is $1,634/month before implementation cost. This is redeployable staff capacity, not cash savings or avoided downtime revenue.

| Sensitivity | Eligible / adoption / resolution | Minutes saved | Successful sessions/month | Capacity value/month | Value less $1,600 recurring cost |
|---|---|---:|---:|---:|---:|
| Conservative | 40% / 50% / 60% | 3 | 396 | $792 | -$808 |
| Base planning case | 60% / 70% / 70% | 5 | 970.2 | $3,234 | $1,634 |
| Favorable | 80% / 85% / 80% | 7 | 1,795.2 | $8,377.60 | $6,777.60 |

At the base volumes, recurring break-even requires 2.47 minutes saved per successful session: $1,600 / 970.2 / $40 x 60. A hypothetical $60,000 implementation would take 36.7 months to recover at the base recurring net value if capacity were fully realized. The base case does not justify committing the full pilot budget now. The initial discovery stage must establish eligible demand, measured task time, usable source coverage, current run-cost quotations and the sponsor's investment hurdle. Stop or improve search alone if a credible case for further investment does not emerge. Larger benefits from support deflection, avoided downtime or retention need separate measurement and must not be added without evidence or overlap checks.

## Twelve-week pilot and stakeholder ask

| Weeks | Work and exit evidence | Lead |
|---|---|---|
| 1 to 2 | Audit documents and catalog applicability; interview authorized technicians; establish search baseline, task eligibility, language needs and privacy/safety requirements. Funding gate: proceed only with usable approved sources, an available safety reviewer and a credible measured business case | PM, domain owner and sponsor |
| 3 to 5 | Build mobile read-only flow, ingestion, filtered retrieval, catalog checks and audit events; freeze prompts and offline test sets | Application and ML engineers |
| 6 to 8 | Independent domain scoring, tenant isolation and injection checks, rollback rehearsal, mobile accessibility and load testing; correct failures before supervised access | Safety, security and QA leads |
| 9 to 10 | Supervised English pilot away from active hazardous work; collect comparable task outcomes and fully loaded costs | Pilot coordinator |
| 11 to 12 | Review all five gates and economics; choose stop, revise or expand. Prepare Spanish validation only if English passes and sufficient bilingual review exists | Sponsor and cross-functional review group |

Proposed staffing if all stages proceed: one application engineer, one ML/retrieval engineer, 0.25 FTE domain expert and 0.25 FTE PM/designer for twelve weeks, totaling 30 person-weeks. A planning rate of $2,000/person-week gives $60,000 labor. Three months of the $1,600 recurring allowance adds $4,800, for a proposed $64,800 full-pilot envelope and a $65,000 ceiling. The recurring allowance includes independent quality review outside those 30 person-weeks. Security and safety sign-off depend on existing reviewers being available within that envelope; re-scope if they are not. The initial two-week stage authorizes at most $10,000 labor plus $1,000 run and review allowance. Its $11,000 cap is part of the $65,000 ceiling, not additional funding; reconcile actual spend before any further release.

Ask the sponsor to authorize only the $11,000 discovery stage now, assign a domain owner and safety reviewer, and authorize access to approved source material in the chosen region. Reserve the remaining twelve-week plan as a conditional option within the total $65,000 ceiling. Further pilot funding and production release each require a later decision based on evidence. None of those approvals is asserted here.
