# LineGuide 2.3.0: exact slide text and speaker notes

Extracted from the actual PPTX. Text inside images is outside this extraction; the PDF and standalone diagrams support visual review.

PPTX SHA-256: `62ef4406d1c2fa0c176f530fb82107e263587ec5685462bbd2d81d0c122424e8`.

## Slide 1: LineGuide

### Visible text

Hypothetical case. Scenario facts, labelled assumptions and synthetic illustrations.
01
LineGuide
AI-powered industrial robot
expert advisor
Scenario C, Udacity ND088
Product proposal v2.3.0, 16 November 2026

### Speaker notes

This is a hypothetical product proposal addressing the supplied ND088 rubric. It does not require an operating company or measured customer telemetry. The deliverable defines the product, risks, system goals, architecture, settings and proposed success measurements. Future research, implementation, contracts and validation are part of the product plan, not completed coursework experiments. The proposed budget begins with USD 11,000 within a conditional USD 65,000 twelve-week plan. AI contributions and source limits are disclosed in the appendix.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 2: Business problem and current baseline

### Visible text

Business problem and current baseline
Source: supplied hypothetical Scenario C; figures are not measured company data
02
Problem
Technicians struggle to find applicable information in an English-only robot knowledgebase.
Today
Keyword search, manual/catalog comparison, then company support.
Given scale
7,500 articles, 25 topics, 15 robot models and 45,000 parts; 150 queries/day.
Evidence gap
Search time, resolution and escalation cost have not been measured.

### Speaker notes

Business problem: Technicians struggle to find the right answer in an English knowledgebase spanning many robot configurations. Unresolved searches consume their time and require company support. Scenario givens are hypothetical, supplied by the assignment. Users are aged 20 to 60; languages: English, Spanish, Cantonese, Mandarin, Urdu. Device access 95% mobile 75% computer 25% tablet and education 85% high school 35% community college overlap and must not be added or normalized. Measure the search baseline in weeks 1 to 2. Quantified friction is the breadth of source material, configuration and language mismatch, not an observed delay or error rate. No baseline performance figure is invented. Discovery compares matched tasks using current keyword search and improved search before assuming LLM value.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 3: Product definition: two sentences

### Visible text

Product definition: two sentences
Proposed benefit; faster or safer outcomes have not been demonstrated
03
Two-sentence product definition
LineGuide is a mobile assistant that explains approved robot references, cites their revision and returns verified catalog records.
It asks for missing configuration and prepares a technician-reviewed support handoff when evidence is missing or a request is hazardous.

### Speaker notes

The product definition is exactly the two visible sentences. Explanations and source links reduce interpretation effort; configuration prompts improve applicability; exact catalog lookup reduces identifier ambiguity; a reviewed handoff preserves support context. These are proposed benefits, not measured results.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 4: Features, benefits and adoption friction

### Visible text

Features, benefits and adoption friction
Hypothetical proposal. Proposed targets remain unmeasured.
04
Required feature
Proposed customer benefit
Friction to test
Configuration + source revision
Applicable, openable references
Repeated setup; wrong model selection
Short answer + exact parts
Less interpretation and ambiguity
Wrong or vague advice erodes trust
Reviewed handoff + staged languages
Support context and wider access
Connectivity and English-only pilot limits
Test adoption and value in supervised tasks; these benefits have not been demonstrated.

### Speaker notes

The table pairs required features with customer benefits and factors reducing appeal. User appeal depends on trust, source applicability, readable mobile output, low entry effort and an obvious path to human support. A language rollout must account for Cantonese separately from Mandarin and right-to-left Urdu UI. Offline generation is unavailable and the MVP does not cache answers. A search-only improvement remains the alternative if the LLM does not pass value and risk gates.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 5: LLM and non-LLM alternatives

### Visible text

LLM and non-LLM alternatives
Hypothetical proposal. Proposed targets remain unmeasured.
05
Dimension
Keyword search
Rules / intent trees
LLM with RAG
Language flexibility
Exact terms and synonyms
Authored intents and branches
Varied phrasing and clarification
Edge-case synthesis
User reconciles documents
Only anticipated cases
Explains retrieved evidence; abstains on conflict
Maintenance
Curate terms and metadata
Update branching logic and tests
Curate sources, prompts and regression tests
Determinism
Repeatable ranking inputs
Explicit rules and exact lookup
Variable generation; validate every answer
Rules retain permissions and exact parts. Measured value must exceed improved search.

### Speaker notes

No application-specific performance has been measured. RAG retrieves grounding material but does not guarantee correct answers or faithful citations. Fine-tuning is deferred: authoritative facts change and remain in retrievable records. Consider it later only for a repeatable behavior gap that prompt/retrieval changes cannot fix, with licensed redacted examples and held-out tests.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R03: RAG and generative AI in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
Source limit: RAG does not guarantee correctness or citation faithfulness. Agentic retrieval exists; choosing classic RAG here is a design judgment for a small, tightly controlled pilot.
R04: Hybrid search overview
https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
Source limit: No application-specific relevance gain or accuracy percentage is established. Part validity still needs deterministic lookup against the authoritative catalogue.

## Slide 6: Existing industrial copilots set the comparison

### Visible text

Existing industrial copilots set the comparison
Hypothetical proposal. Proposed targets remain unmeasured.
06
Option
Documented capability
Implication
Siemens Maintenance Copilot
Linked manuals and maintenance records; web/mobile
Adjacent competitor; mobile requires online mode
ABB Genix APM Copilot
Conversational operational information
Established category; no head-to-head result available
LineGuide proposal
Robot/version filters and exact catalog checks
Differentiation remains untested
Installed-base support need is the opportunity. Revenue and market size remain unestimated.

### Speaker notes

Siemens source is Asset Essentials Enterprise Maintenance Copilot documentation. ABB source is its Genix APM Copilot product page. These vendor sources establish capabilities, not measured superiority or transferable downtime reduction. The existing English knowledgebase plus human escalation remains the current comparison. No competitor pricing or willingness-to-pay research was conducted.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R07: Maintenance Copilot documentation
https://help.assetmanagement.siemens.com/help/Content/Documentation/Maintenance/Asset%20Essentials/EnterpriseFeatures/AI-Driven%20Capabilities/Maintenance%20Copilot.htm
Source limit: This is vendor documentation, not independent comparative testing. It establishes an adjacent competitor; it does not prove the proposed product is uniquely capable or faster.
R08: Genix APM Copilot
https://new.abb.com/process-automation/genix/abb-genix-copilot/apm
Source limit: Claims about speed and downtime on this vendor page are not transferred into the proposal as measured benefits. No head-to-head evaluation or pricing comparison was conducted.

## Slide 7: System attributes: goals and pilot scope

### Visible text

System attributes: goals and pilot scope
Proposed scope; document suitability and language performance are untested
07
Primary system goal
Supervised English pilot
Increase verified self-service resolution of eligible reference and catalog questions.
Secondary goals
1. Reduce time to a verified answer.
2. Prevent unsupported or hazardous assistance.
Two models, up to 200 approved articles across five topics.
Read-only explanations and catalog lookup. Each later language requires its own validation.

### Speaker notes

System attributes required by the rubric: one primary goal and two secondary goals. Initial audience: authorized maintenance technicians reviewing reference information away from active hazardous work. English only at initial pilot. Later Spanish, Mandarin, written Cantonese and Urdu each need their own technical language validation; Cantonese must not be treated as Mandarin and Urdu needs right-to-left UI testing. Voice is outside the MVP. Pilot coverage is a proposed scope, not the actual distribution of source documents.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 8: Runtime query and response flow

### Visible text

Runtime query and response flow
Proposed architecture. Solid arrows carry data; dashed arrows carry support or audit events.
08
Private application and data services
Provider processing boundary
Mobile client
Entra ID
API orchestrator
Policy gateway
Hybrid search index
Generation endpoint
Response validator
Parts catalogue
Human support
Audit store
TLS
OIDC / TLS
Draft
Read-only lookup
Validated answer or abstention
Validated result
Blocked / missing evidence
Metadata
Service links use TLS 1.2+, private endpoints and managed identities where supported. Controllers are unreachable.

### Speaker notes

Proposed runtime components: Mobile client, Entra ID, API orchestrator, Policy gateway, Hybrid search index, Generation endpoint, Response validator, Parts catalogue, Human support, Audit store. Mobile client crosses the public edge over authenticated TLS. Entra ID issues identity claims checked by API orchestrator. Policy gateway derives tenant and entitlements on the server, minimizes sensitive prompt content and refuses prohibited work before retrieval. Hybrid search index returns permitted current passages. Generation endpoint drafts a cited explanation. Response validator rechecks entitlements, citations, revision and exact permitted Parts catalogue records before API orchestrator returns a validated response or abstention to Mobile client. Policy gateway sends blocked or missing-evidence requests to Human support after the technician reviews the context; Human support returns status via API orchestrator. Outage or timeout makes the API show an unavailable state and the established support route, with no new generated answer. Response validator emits filtered metadata to Audit store. All depicted network connections use TLS 1.2 minimum (target 1.3 when supported), authenticated authorization and private service connectivity where available. The provider processing boundary requires separate geography and retention review. No controller credentials or network route exist. AES-256 at rest, RBAC and retention controls are defined in CONFIGURATION.md and the component register. Arrows are logical flows, not proof of a deployed network.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R03: RAG and generative AI in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
Source limit: RAG does not guarantee correctness or citation faithfulness. Agentic retrieval exists; choosing classic RAG here is a design judgment for a small, tightly controlled pilot.
R04: Hybrid search overview
https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
Source limit: No application-specific relevance gain or accuracy percentage is established. Part validity still needs deterministic lookup against the authoritative catalogue.
R05: Security filters for trimming results in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
Source limit: String filtering is an application-enforced pattern, not automatic identity authorization. Server-side construction, deny-by-default behavior, tenant boundaries and leakage tests remain implementation requirements.
R06: Data, privacy, and security for Models sold by Azure in Microsoft Foundry
https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
Source limit: No zero-retention or unconditional single-region guarantee follows. Customer-specific contract and deployment acceptance remain unverified. Privacy and legal review must precede customer-data use; no compliance or safety certification is established.

## Slide 9: LLM deployment and configuration

### Visible text

LLM deployment and configuration
Candidate version is documented; account access, quality, latency and configuration are untested
09
Property
Proposed setting
Candidate
Azure gpt-6-astra, version 2026-09-03; documented, untested candidate
Generation
Responses API; reasoning low; temperature 0.1; output cap 2,000 tokens
Application limits
All input ≤8,000 tokens; visible target ≤800; 15-second deadline; no auto-retry
Privacy and grounding
store=false; request-only context; RAG for manuals; exact SQL parts
Vendor interfaces are documented. Access, latency, behavior, price and safety remain untested.

### Speaker notes

Every value is a proposed starting setting. Microsoft R01 and R12 list gpt-6-astra version 2026-09-03 with temperature support. Use reasoning effort low and temperature 0.1 to limit generation variability, without asserting determinism or correctness. Benchmark whether the candidate meets quality, latency and cost gates; account access, deployment geography, quota and endpoint behavior remain untested. Sum the system, user, retrieval and tool inputs into an 8,000-token input cap. The 2,000 output cap includes reasoning, with a visible answer target of 800 tokens. At output truncation, timeout or validation failure return abstention or escalation, never an unvalidated partial response. store=false avoids persisted Responses API response state; avoid conversations and previous_response_id. These settings do not remove separate provider abuse-monitoring retention. Privacy and service contracts must be approved before proprietary input. RAG keeps changing facts in versioned approved records; do not fine-tune weights for the catalog. No live model inference has been run. Current Microsoft and OpenAI publisher documentation corroborate the candidate. The assessment assertion that it does not exist is not supported by those pages. A dated Azure model version differs from a deployment name, which is the request model value. Suggested older substitutes have lifecycle constraints; do not infer account availability from a catalog. R13 and R14 record model and lifecycle evidence. Source checks are not model evaluations.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R01: Azure OpenAI reasoning models
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning
Source limit: These documented interfaces and ceilings do not establish account access, deployment availability, price, latency, quality or safety. The application caps, temperature 0.1 and reasoning effort low are proposed settings that require endpoint and held-out evaluation.
R12: Use the Azure OpenAI Responses API
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses
Source limit: store=false is not a blanket zero-retention guarantee. Abuse-monitoring and contractual review remain separate. This source does not establish customer resource access, regional availability, or tested runtime behavior.
R13: GPT-6 Astra model
https://developers.openai.com/api/docs/models/gpt-6-astra
Source limit: The direct OpenAI alias is gpt-6-astra. Azure version 2026-09-03 is identified by Microsoft and must not be presented as an OpenAI snapshot identifier. OpenAI pricing and access statements do not constitute an Azure quote or prove subscription access, runtime performance or industrial suitability.
R14: Azure model retirement schedule and lifecycle policy
https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule
Source limit: No Astra row or retirement date was found in the inspected schedule. That absence does not establish a retirement date, perpetual availability or the status of a customer deployment. Model lifecycle and regional availability must be checked for the actual subscription before selection or provisioning.

## Slide 10: Five risks and accountable mitigations

### Visible text

Five risks and accountable mitigations
Hypothetical proposal. Proposed targets remain unmeasured.
10
Risk
Mitigation
Owner
Harmful or poor advice
Block hazardous requests; preserve warnings; common-sense review; suspend on critical escape
Safety lead
Wrong revision or part
Require configuration; filter approved records; exact-match every emitted part
Content owner
Factory data leakage
Server-side entitlements, prompt minimization, isolation tests and approved provider terms
Security lead
Language / user bias
Review novice tasks and each enabled language/model group; stage language releases
Localization lead
Low value / rising cost
Compare search; cap tokens/concurrency; reserve cost; alert at 80%, stop at 100% of $800 cloud allowance
Product manager
Inaction keeps search and support friction and may cede capability to existing copilots; the monetary impact is unknown.

### Speaker notes

These are five product risks, not an exhaustive safety assessment. The service has no controller connection and cannot authorize physical work or order parts. Ambiguous hazardous requests receive escalation. Qualified personnel retain responsibility for physical work. A critical escape suspends the affected capability for safety review. Delaying experimentation preserves current search friction and escalation, but their monetary size is unknown. A bounded discovery stage tests whether an LLM adds enough value to justify its operating and review costs. Each risk has a controllable product or engineering mitigation, not a promise to remove all risk. Common-sense review includes prerequisite clarity and relevance for less experienced technicians. Evaluate bias by language, experience and robot model. The USD800 cloud ceiling is a proposed allowance, not a quotation; alert at USD640 and stop new generation at USD800 while retaining search/support. Restrict service quotas, reconcile delayed billing and reserve expected in-flight cost before accepting requests; cloud budget alerts alone cannot enforce a hard cap. No automatic generation retries and no response cache in the MVP. These operating controls must be implemented and tested.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R09: Industrial robot systems and industrial robot system safety
https://www.osha.gov/otm/section-4-safety-hazards/chapter-4
Source limit: The manual is technical guidance for inspection and hazard understanding, not certification of a chatbot. Local obligations and current applicable standards require qualified safety/legal review.

## Slide 11: Success measures: customer outcomes

### Visible text

Success measures: customer outcomes
Two of five proposed measurements. Baselines and outcomes are not yet measured
11
Measurement
Definition and proposed gate
Pilot evidence
Verified self-service resolution
Confirmed correct resolution, no escalation within 24 h / all eligible sessions; ≥70%
≥200 eligible sessions; review all outcomes
Time to verified answer
Median time to correct answer or appropriate escalation; ≥30% lower than search
25 technicians; 200 trials/condition; counterbalanced
Abstentions, missing feedback and escalations remain in the resolution denominator.

### Speaker notes

Resolution numerator: eligible sessions with technician-confirmed resolution, domain-review confirmation and no support escalation within 24 hours. Denominator: all eligible sessions, including abstentions, missing feedback and escalations. Use the same eligibility for search. For task time, 25 technicians complete 16 trials each, eight search and eight assistant, using distinct matched variants and counterbalanced order. This yields 200 trials per condition. Report paired differences and uncertainty alongside completion and escalation rates. This pilot screen does not prove population-wide lift. Report every KPI by enabled language and robot model. All targets are proposed and unmeasured.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 12: Success measures: quality and reliability

### Visible text

Success measures: quality and reliability
Three of five proposed measurements. No model result or load test has been observed
12
Measurement
Proposed gate
Evidence and response
Evidence and parts
≥98% correctness; 0 wrong parts; ≥76/80 known record returns; 20/20 ambiguous clarifications
≥200 substantive answers; domain review; abstentions fail known cases
Prohibited-assistance escape
0 observed escapes / 100 prohibited cases per language
Any critical escape suspends affected capability
Validated latency, p95
≤8 seconds; failures and timeouts exceed target
≥500 requests at 10 concurrent users; 15-second timeout
Zero observed safety escapes in curated tests does not certify industrial safety.

### Speaker notes

Correctness numerator: substantive answers whose material claims have applicable current cited support and whose emitted parts exactly match compatible permitted catalog records. Denominator: all substantive answered cases. Require at least 200 substantive answers and at least 98% correctness. The 100 catalog cases contain 80 unique known parts and 20 ambiguous or unknown cases. Require at least 76/80 correct record returns, 20/20 appropriate clarifications or escalations, and zero wrong part emissions. Abstentions count as failed known-record returns. Safety escape rate is actionable prohibited assistance divided by all prohibited requests. Require zero observed escapes in 100 cases per language and no critical escape in supervised use. Zero of 100 would imply an approximate 3% upper 95% bound only with independent representative sampling; curated tests do not meet that assumption or certify safety. Latency is empirical p95 from server acceptance to fully validated response or abstention; failures and timeouts exceed the target. Use 500 requests at 10 concurrency and record query mix, cache state and versions.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 13: Proposed validation plan

### Visible text

Proposed validation plan
Proposed acceptance plan. Tests and customer studies remain to be run
13
Freeze tests
400 proposed English cases: 200 routine, 100 catalog and 100 prohibited requests.
Review independently
Domain reviewers score support and parts; safety lead adjudicates escapes.
Verify failures
Test isolation, injection, outages, expiry and rollback before supervised use.
Compare tasks
Matched search/assistant tasks and full operating cost; thresholds remain unmeasured.

### Speaker notes

The English release set has 400 disjoint semantic cases: 200 routine, 100 catalog and 100 prohibited requests. The catalog split is 80 unique known records and 20 ambiguous or unknown cases, with the subgates on the quality and reliability measures. These are proposed tests, not executed results. Customer tasks and catalogs are unavailable; qualified reviewers must create and approve them. Freeze the release set before tuning. The separate 500 request load test uses a pinned deployment. Test 1,500 requests/day before claiming tenfold headroom over the scenario 150 daily. Block delivery until validation completes. Each later language repeats its own semantic and safety validation. An LLM cannot be the sole grader of itself. These are future implementation tests, not requirements to have completed real-world experiments for this hypothetical course proposal.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 14: Synthetic illustration: current support demand

### Visible text

Synthetic illustration: current support demand
Synthetic data. No real customer or CRM records are represented.
14
Generated outcome
Sessions
Share
Self-service resolution
485
32.33%
OEM support escalation
605
40.33%
Abandonment / local workaround
410
27.33%
1,500 generated sessions; seed 20261116. A reproducible illustration using stated parameters.

### Speaker notes

The supplied final generator creates a synthetic frame of 1,500 sessions and a 240-record timed sample using 15 invented domain/family strata. Reproduction matched CSV SHA-256 cef03be7adb723bab005ea3d5ab679c3f418910d5f2612f5f7eccd74c9013de2. Generated outcomes are 485 resolved, 605 escalated and 410 abandoned/workaround; percentages round to 99.99%. Sample mean search time is 22.8153776071 minutes; generated escalated-ticket mean support time is 29.6086305292 minutes. These are simulation outputs, not company logs, observed customer performance, causal language effects or measured LLM benefits. All distributions, rates, group mappings and language penalties are assumptions. Customer search labor and OEM support labor have different owners; their assumed dollar rates do not establish payroll or cash savings. The simulation supports transparent proposal reasoning without requiring a real business. See docs/SYNTHETIC-BASELINE-AUDIT.md, source/synthetic-baseline.py and simulation/.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 15: Illustrative business value

### Visible text

Illustrative business value
Planning assumptions in USD. Proposed value has not been measured.
15
Planning assumptions
Illustrative monthly value
150 queries/day (scenario given).
22 service days, 60% eligibility, 70% adoption and 70% verified resolution (assumed).
5 minutes saved/session and $40/hour capacity value (assumed).
970.2 successful assisted sessions.
$3,234 capacity value less $1,600 assumed run cost gives $1,634 net capacity value.
Sensitivity and implementation costs appear in the appendix.
Scenario-based estimate. Saved time creates capacity value only when it can be redeployed.

### Speaker notes

Currency: USD. Only 150 queries/day is supplied by the scenario. The 22 service days, eligibility 60%, adoption 70%, resolution 70%, five minutes saved and $40/hour are assumptions. Exact calculation: 150*22*.6*.7*.7= 970.2; 970.2*5/60*40=3234. Recurring cost 800 + 16*50=1600; base net 1634. The $800 cloud/search/storage/model allowance is not a vendor quote and must be replaced with a confirmed Azure estimate. This is redeployable staff capacity, not cash savings, avoided downtime, revenue or a forecast. A query is not a unique technician. Do not add support/downtime benefits without separate measurement and overlap checks. The illustrative calculation is 970.2 successful sessions/month × (5 minutes/session ÷ 60 minutes/hour) × USD 40/hour = USD 3,234/month; the unit conversion is explicit here in the notes. The dimensional calculation is successful sessions × minutes/session ÷ 60 minutes/hour × USD/hour. All values other than 150 daily queries are assumptions. The sensitivity appendix preserves the three cases and budget arithmetic. No cash-savings, downtime, revenue, user-interview or paid-customer result is claimed. The hypothetical assignment permits proposed assumptions and clearly labelled illustrative data. Real customer measurements are not a prerequisite for producing the requested proposal. This planning case is separate from the supplied synthetic baseline; its different rates and adoption assumptions are not silently combined.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 16: Proposed rollout and stakeholder decision

### Visible text

Proposed rollout and stakeholder decision
Proposed implementation roadmap. Tests and approvals would occur after the proposal.
16
Weeks 1-2
Confirm assumptions, source access and scope; proposed first-stage budget: $11,000.
Weeks 3-5
Build read-only RAG, exact catalog validation and audit events.
Weeks 6-10
Run planned quality, safety and load tests, then supervised English use.
Weeks 11-12
Review all five measures and economics; choose stop, revise or language expansion.
Proposed twelve-week ceiling: $65,000. Funding and rollout are stakeholder decisions in this hypothetical plan.

### Speaker notes

Authorize only the first two weeks now: at most USD 10,000 labor plus USD 1,000 run and independent-review allowance. This USD 11,000 cap is included in the conditional total USD 65,000 ceiling. If all stages proceed, staffing is one application engineer, one ML/retrieval engineer, 0.25 FTE domain expert and 0.25 FTE PM/designer for twelve weeks: 30 person-weeks at USD 2,000 = USD 60,000. Three months recurring allowance adds USD 4,800, giving USD 64,800. Independent quality review is outside the 30 person-weeks. Existing safety/security reviewers must fit the envelope; otherwise re-scope. Reconcile actual discovery spend before releasing more funding. Weeks 6 to 8 cover independent quality, isolation, injection, accessibility, load and rollback tests; weeks 9 to 10 are supervised English use away from active hazardous work. Spanish needs separate bilingual validation. The sponsor should assign domain and safety reviewers and authorize approved sources in the selected region. No funding, source access or production approval is asserted. The roadmap describes future work inside the fictional scenario. An actual business, approved budget, completed customer study or production service is not required to complete this proposal deliverable.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 17: Offline approval, indexing and revocation

### Visible text

Offline approval, indexing and revocation
Appendix. Offline ingestion changes approved versions; runtime retrieval uses only the active approved version.
17
Private ingestion and data boundary
Provider embedding boundary
Approved source store
Ingestion worker
Embedding endpoint
Hybrid search index
Parts catalogue
Audit store
Approved catalog records
Revision, approval and deletion events
TLS 1.2+ and managed identities protect each link. AES-256 and scoped RBAC protect every stored record.

### Speaker notes

Proposed offline components: Approved source store, Ingestion worker, Embedding endpoint, Hybrid search index, Parts catalogue, Audit store. Content owners approve revisions and model/firmware/language/entitlement metadata in Approved source store before publication. Ingestion worker rejects missing or withdrawn approvals, preserves complete warnings, chunks near 500 tokens with 80-token overlap and calls Embedding endpoint. Hybrid search index stores versioned vectors and searchable text. Parts catalogue holds exact authoritative records separately from document chunks; embeddings never establish part validity. A withdrawal event removes matching index and catalogue versions, cancels in-flight applicability and triggers the runtime validator to reject stale citations. Audit store records filtered revision/deletion metadata. Failures quarantine the new version and preserve only a separately approved current index; no partial index promotion. Initial answer caching is disabled. Owners must test revocation before enabling offline reference caching or scoped response caching. Proposed index version promotion and rollback are atomic and evaluated before pilot use. All listed component names match the diagram and docs/components.json. No source system, embedding endpoint or index has been provisioned.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R03: RAG and generative AI in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
Source limit: RAG does not guarantee correctness or citation faithfulness. Agentic retrieval exists; choosing classic RAG here is a design judgment for a small, tightly controlled pilot.
R04: Hybrid search overview
https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
Source limit: No application-specific relevance gain or accuracy percentage is established. Part validity still needs deterministic lookup against the authoritative catalogue.
R05: Security filters for trimming results in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
Source limit: String filtering is an application-enforced pattern, not automatic identity authorization. Server-side construction, deny-by-default behavior, tenant boundaries and leakage tests remain implementation requirements.
R10: Understand embeddings in Azure OpenAI
https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/understand-embeddings
Source limit: The page is marked Foundry classic. Confirm current deployment support and model version before provisioning. Embedding retrieval does not validate exact part identifiers or language quality.

## Slide 18: Retrieval, validation and capacity limits

### Visible text

Retrieval, validation and capacity limits
Appendix. Starting retrieval settings; held-out evaluation decides whether to change them
18
Ingest controlled records
Preserve owner, revision, section, model, firmware, language and entitlement metadata.
Retrieve applicable evidence
Start near 500-token sections with 80-token overlap; hybrid top 20, rerank to at most five passages.
Validate before display
Confirm cited revisions and compatibility; exact-match every emitted part to permitted records.
Capacity and failure
Scale API workers and the search tier only after tests; rate-limit requests and escalate on outage.

### Speaker notes

These chunking and retrieval values are proposed starting settings. Keep warnings attached to their sections. Reject withdrawn records and missing approval or applicability metadata. The structured parts catalog is separate from document chunks; embeddings cannot establish part validity. Pin model, prompt, embedding and index versions together, and rehearse rollback. If caching is enabled after pilot revocation testing, cache only within tenant and permission scope. The embedding candidate is text-embedding-3-small; verify its current Azure region/version support and retrieval quality before use. Per-session and per-tenant quotas, a proposed maximum ten active requests, a 15-second deadline and no automatic generation retries bound load. Validate 500 requests at ten concurrency and 1,500 daily requests before asserting headroom; 150/day is scenario demand, not measured throughput. Initial answer caching is disabled to avoid permission and revision leaks. Missing, conflicting or withdrawn content still requires clarification or escalation.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R03: RAG and generative AI in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
Source limit: RAG does not guarantee correctness or citation faithfulness. Agentic retrieval exists; choosing classic RAG here is a design judgment for a small, tightly controlled pilot.
R04: Hybrid search overview
https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
Source limit: No application-specific relevance gain or accuracy percentage is established. Part validity still needs deterministic lookup against the authoritative catalogue.
R05: Security filters for trimming results in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
Source limit: String filtering is an application-enforced pattern, not automatic identity authorization. Server-side construction, deny-by-default behavior, tenant boundaries and leakage tests remain implementation requirements.
R10: Understand embeddings in Azure OpenAI
https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/understand-embeddings
Source limit: The page is marked Foundry classic. Confirm current deployment support and model version before provisioning. Embedding retrieval does not validate exact part identifiers or language quality.

## Slide 19: Security and privacy requirements

### Visible text

Security and privacy requirements
Appendix. Requirements before customer-data use; no compliance or certification claim
19
Control data access
Constrain external processing
Server-derived tenant identity and least-privilege RBAC.
Filter retrieval and recheck before delivery.
TLS 1.2+ in transit; AES-256 at rest.
Private endpoints and managed identities where supported.
store=false; request-only app context.
No raw-query logs or persistent conversation state.
Audit metadata: proposed 30-day retention, delete within the next 24 hours.
Provider retention and processing geography require approval.
Azure’s no-training statement does not establish zero retention or safety certification.

### Speaker notes

Proposed controls, not deployed facts. Device sessions use Entra identity and a 15-minute inactivity expiry; request text stays in memory only for request processing and is not saved by the application. No raw query or response content enters audit storage; use pseudonymous request identifiers, timings, version IDs, policy outcome and reviewer disposition. Retain metadata for 30 days and delete within the following 24-hour lifecycle window. Delete tenant data and embeddings within seven days of an authorized deletion request, subject to documented legal retention exceptions; contractual and backup deletion obligations need verification. AES-256 at rest and RBAC apply to source, search, catalog and audit stores. Private endpoints and managed identities apply where each Azure service supports them; Entra and public device entry are authenticated internet boundaries. A private endpoint does not establish processing residency or zero retention. Provider abuse monitoring and legal/security terms remain separate prerequisites. Test isolation, injection, revocation, deletion and least privilege before customer data.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
References:
R05: Security filters for trimming results in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
Source limit: String filtering is an application-enforced pattern, not automatic identity authorization. Server-side construction, deny-by-default behavior, tenant boundaries and leakage tests remain implementation requirements.
R06: Data, privacy, and security for Models sold by Azure in Microsoft Foundry
https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
Source limit: No zero-retention or unconditional single-region guarantee follows. Customer-specific contract and deployment acceptance remain unverified. Privacy and legal review must precede customer-data use; no compliance or safety certification is established.
R09: Industrial robot systems and industrial robot system safety
https://www.osha.gov/otm/section-4-safety-hazards/chapter-4
Source limit: The manual is technical guidance for inspection and hazard understanding, not certification of a chatbot. Local obligations and current applicable standards require qualified safety/legal review.

## Slide 20: Scenario C: given facts and evidence limits

### Visible text

Scenario C: given facts and evidence limits
Appendix. Given assignment context. Search performance and product outcomes remain unmeasured.
20
Technicians
Ages 20–60; 85% high school and 35% community college, with overlapping attainment.
Languages
English, Spanish, Cantonese, Mandarin and Urdu; knowledgebase currently English-only.
Device access
95% mobile, 75% computer and 25% tablet. Shares overlap and are not a distribution.
System scale
7,500 articles, 25 topics, 150 queries/day, 45,000 parts and 15 robot models.

### Speaker notes

All values on this slide are immutable hypothetical assignment facts, not customer measurements. Scenario A/B figures are excluded. Slow search and staff escalation describe the supplied workflow; no measured task latency, user research, adoption or deployed performance is available. Targets, budgets, architecture settings and rollout choices elsewhere are proposed assumptions. Source: user-supplied Scenario C and reconciled checklist. Do not add overlapping education/device percentages or treat queries as unique users.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 21: Sensitivity and investment discipline

### Visible text

Sensitivity and investment discipline
Appendix. Scenarios are sensitivity cases; ranges are not statistical confidence intervals
21
Planning case
Sessions/month
Capacity value
Less $1,600 run cost
Conservative: 3 min saved
396
$792
−$808
Base: 5 min saved
970.2
$3,234
$1,634
Favorable: 7 min saved
1,795.2
$8,377.60
$6,777.60
Base recurring break-even: 2.47 minutes saved/session. $60,000 labor payback: 36.7 months.

### Speaker notes

All cases use 150 queries/day, 22 days/month and USD 40/hour. Conservative assumptions: 40% eligible, 50% adoption, 60% resolution, three minutes saved. Base: 60%, 70%, 70%, five minutes. Favorable: 80%, 85%, 80%, seven minutes. Monthly run cost is assumed USD 1,600 in all cases. Base recurring break-even: 1600/970.2/40*60=2.47371676 minutes. Simple labor-only implementation payback: 60000/1634=36.7197 months, excluding pilot run allowance, financing and ramp effects. This weak standalone case does not justify committing the full pilot now. Discovery must establish measured demand, task time, source coverage, current quotations and the sponsor investment hurdle; otherwise stop or improve search alone. Capacity creates value only if it can be redeployed.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 22: References: design, configuration and privacy

### Visible text

References: design, configuration and privacy
Appendix. Primary vendor sources and assignment background. Access limits are recorded in sources.json.
22
R01  Azure OpenAI reasoning models
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning
R02  How to generate reproducible output with Azure OpenAI in Microsoft Foundry Models (classic)
https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/reproducible-output
R03  RAG and generative AI in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
R04  Hybrid search overview
https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
R05  Security filters for trimming results in Azure AI Search
https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
R06  Data, privacy, and security for Models sold by Azure in Microsoft Foundry
https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
R13  GPT-6 Astra model
https://developers.openai.com/api/docs/models/gpt-6-astra

### Speaker notes

Source access and limits are recorded in docs/sources.json. HBR is metadata/preview only. Model existence and interface documentation do not prove account access, quality, latency, price or industrial safety.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 23: References: market and scenario background

### Visible text

References: market and scenario background
Appendix. Primary vendor sources and assignment background. Access limits are recorded in sources.json.
23
R07  Maintenance Copilot documentation
https://help.assetmanagement.siemens.com/help/Content/Documentation/Maintenance/Asset%20Essentials/EnterpriseFeatures/AI-Driven%20Capabilities/Maintenance%20Copilot.htm
R08  Genix APM Copilot
https://new.abb.com/process-automation/genix/abb-genix-copilot/apm
R09  Industrial robot systems and industrial robot system safety
https://www.osha.gov/otm/section-4-safety-hazards/chapter-4
R10  Understand embeddings in Azure OpenAI
https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/understand-embeddings
R11  How to Train Generative AI Using Your Company’s Data
https://hbr.org/2023/07/how-to-train-generative-ai-using-your-companys-data
R12  Use the Azure OpenAI Responses API
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses
R14  Azure model retirement schedule and lifecycle policy
https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirement-schedule

### Speaker notes

Source access and limits are recorded in docs/sources.json. HBR is metadata/preview only. Model existence and interface documentation do not prove account access, quality, latency, price or industrial safety.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.

## Slide 24: Scenario basis and AI assistance

### Visible text

Scenario basis and AI assistance
Source limits, assumptions and reproducibility records accompany the proposal.
24
Scenario basis
Scenario C facts are supplied; targets, budgets and rollout choices are proposed.
Synthetic illustration
A fixed-seed generator creates demonstration data with a verified dataset hash.
AI assistance
AI contributed substantive reasoning, architecture, calculations, prose, diagrams and code.
Hand-in status
The repository contains proposal assets. No classroom submission or own-work attestation was performed.

### Speaker notes

The current proposal is built for the hypothetical ND088 scenario and its actual rubric. Clearly labelled assumptions and synthetic data are included without representing them as empirical customer measurements. AI contributions extend beyond copy editing and layout. Human authorship or universal human verification is not asserted. The user reported no course-specific permission; the package makes no eligibility or own-work attestation and records no classroom submission. These provenance facts remain separate from product planning and artifact completeness. Future business validation does not become a new course completion requirement.
Evidence status: Design proposal. No operational model test, user study or deployment has been run.
