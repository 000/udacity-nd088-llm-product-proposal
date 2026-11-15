# Component and connection register

Version 1.1.0. These are proposed logical components. Their IDs and labels match the runtime and controlled-ingestion diagrams; implementation services may sit within a logical component.

| ID | Exact diagram label | Responsibility and implementation boundary |
|---|---|---|
| C1 | Mobile web client | Responsive technician interface; displays configuration, validated answers, source links and escalation. No robot-control credentials or persistent raw-query storage |
| C2 | Identity and policy API | Validates Entra identity, derives tenant entitlement, requires model/firmware, applies task policy, orchestrates the request and returns the result |
| C3 | Hybrid retrieval | Azure AI Search keyword/vector retrieval over the approved index; server-derived tenant, configuration and current-revision filters |
| C4 | Generation endpoint | Approved Azure OpenAI deployment produces a bounded cited draft; no robot-control or autonomous execution authority |
| C5 | Response validator | Checks retrieved citations, current revision, applicability and exact catalog records before releasing an answer or abstention |
| C6 | Controlled manuals | Content-owner-approved originals, revision register and controlled procedure viewer, backed by protected document storage |
| C7 | Parts catalogue | Authoritative relational catalog; read-only compatible-record lookup. The model cannot create identifiers or authorize orders |
| C8 | Human support | Existing qualified support route; any context packet is reviewed by the technician before transmission |
| C9 | Ingestion job | Approval checks, parsing, section-aware chunks, embedding calls and versioned index publication. The embedding deployment needs the same approved data-processing boundary |
| C10 | Audit events | Privacy-filtered request, validation and ingestion metadata; no raw prompts by default; proposed 30-day metadata retention |

## Runtime flows

1. C1 sends a request to C2 over authenticated TLS. C2 derives access scope from validated identity, not prompt text.
2. C2 requests filtered passages from C3 and compatible records from C7. Private service connections, managed identities and least privilege protect backend access.
3. C3 supplies selected grounding to C4 through the orchestrator. C4's draft reaches C5; exact records from C7 also reach C5. These arrows express logical data flow, not independent user-accessible endpoints.
4. C5 releases the validated result or abstention to C2; C2 returns it to C1 over TLS. Failed validation prevents draft display.
5. C2 routes prohibited, hazardous, uncertain or unresolved requests to C8. The product does not authorize physical work. C2/C5 send minimized outcome events to C10.

## Ingestion and withdrawal flows

C6 supplies approved originals and applicability metadata to C9. C9 rejects missing permissions or revision metadata, attaches warnings to their passages, embeds approved content and publishes a versioned index to C3. It records approval/index events in C10. Withdrawal invalidates the index and affected caches; C5 checks current approval before display. C7 remains outside vector retrieval and is queried through its structured interface.

All backend connections require encrypted transport, scoped service identities and private connectivity where supported. Model and embedding processing still require approved geography and contractual review; private endpoints do not imply zero provider retention. No component connects to robot controllers.

During an outage, C1 shows the established support route and produces no new answer. Offline access to private cached manuals is disabled in the pilot. Any later cache capability requires a separate design and tests for permission expiry and withdrawal behavior.
