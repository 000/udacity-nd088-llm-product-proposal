# Component and connection controls

All controls are proposed requirements. The names below match the two editable diagrams and `components.json`. The runtime diagram is slide 8; offline approval and indexing is slide 17.

| Component | Data and access boundary |
| --- | --- |
| Mobile client | Authorized technician session; no offline answer cache; Entra sign-in and inactivity expiry |
| Entra ID | Authenticated identity claims; API verifies tokens and derives tenant/groups server-side |
| API orchestrator | Tenant/request quotas, total input budget and deadline; no controller route or credentials |
| Policy gateway | Enforce entitlements, minimize sensitive prompt content and refuse prohibited requests |
| Hybrid search index | Current approved revisions only; entitlement filters; encrypted store and scoped identity |
| Generation endpoint | Provider processing boundary; minimized context, `store=false`, no autonomous tools; contract/geography approval required |
| Response validator | Recheck permission, citation, revision and exact permitted part identifiers before delivery; reject incomplete output |
| Parts catalogue | Read-only structured records; exact compatibility and entitlement checks; encrypted store and RBAC |
| Human support | Authorized enterprise support; technician reviews context before sharing; existing safety route retained |
| Audit store | Pseudonymous version/timing/policy metadata; no raw query/answer; encryption, restricted review access and retention lifecycle |
| Approved source store | Content-owner approval, revision, warning, applicability, language and entitlement metadata; encryption and RBAC |
| Ingestion worker | Reject incomplete/withdrawn approvals; atomic index promotion and rollback; least privilege |
| Embedding endpoint | Provider boundary for approved source text; approved terms/geography; no inference before privacy review |

Every depicted network link requires TLS 1.2 or later, with TLS 1.3 where supported. Service links require managed identity and private endpoints where the chosen service supports them. Device entry and Entra identity remain authenticated internet boundaries. Private connectivity does not establish processing residency or zero retention. AES-256 at rest and least-privilege RBAC protect the source, index, catalogue and audit stores.

The runtime diagram includes the validated response path back to the API and client, exact catalogue validation, support escalation and metadata events. Its dashed lines carry support/audit events. The ingestion diagram separates content approval, embedding, indexing, catalogue updates and revision events. Withdrawal invalidates active applicability and pending responses. An ingestion failure quarantines the new version; it does not promote a partial index.

On timeout or network failure, the API shows an unavailable state and the established support route. It generates no new answer. Offline caching remains disabled until permission expiry, revision revocation and deletion behavior have been validated. These are logical data-flow diagrams, not evidence of a deployed or certified network.
