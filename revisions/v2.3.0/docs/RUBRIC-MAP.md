# Actual ND088 rubric map

Revision 2.3.0. The controlling source is the project brief, Task List, How to Complete This Project and Project Rubric supplied by the user, reviewed on 16 November 2026. The assignment expressly uses hypothetical business scenarios and asks for a product plan and persuasive presentation. It does not require an operating company, real customer telemetry, a live LLM benchmark, implemented safety controls or production approval.

The seven rubric criteria and the separate submission-format instruction map to this candidate as follows. This is evidence of coverage, not a Udacity grade guarantee.

| Supplied criterion | Requirement, paraphrased | Candidate evidence |
| --- | --- | --- |
| Describe the problem | Simple business problem, today's customer workflow and its main limitations. | Slide 2: English-only keyword search, manual/catalog comparison and support escalation. Slide 20 preserves the Scenario C facts. |
| Describe the solution | A clear 1-3 sentence definition; benefits and necessary features; appeal/friction and improvement over today's approach. | Slide 3 contains two definition sentences. Slide 4 pairs features, benefits and friction. Slides 5-6 explain LLM versus non-LLM alternatives and market context. |
| Identify risks and mitigations | Three to five realistic, controllable risks with a mitigation for each. | Slide 10 contains exactly five owned risk/control pairs, covering technician harm/common-sense advice, wrong parts/revisions, data leakage, bias and value/cost. It also covers the cost of inaction. |
| System Attributes | One primary goal and one or two secondary goals. | Slide 7 names verified self-service resolution as primary, with time to a verified answer and prevention of unsupported/hazardous assistance as two secondary goals. |
| System Architecture | Components, relationship diagram and relevant protected components/connections with controls. | Slides 8 and 17 show runtime and ingestion relationships. The component register uses the same 13 names. Slides 9/19 and the configuration record describe protected links, stores, access and provider boundaries. |
| LLM Configuration | Ideal settings and properties suited to the product goals. | Slide 9 and CONFIGURATION.md specify the proposed deployment/model, API, temperature, input/output budgets, deadline, privacy state and RAG strategy. Sources support the interface claims; future evaluation is part of the proposed implementation plan. |
| Success Metrics | Three to five measurements defining success or failure for user needs. | Slides 11-12 and metrics.json define exactly five measurements with methods and proposed targets. Slide 13 explains proposed evaluation; slide 14 presents a clearly labelled synthetic illustration. |
| Public repository/default branch | Upload the completed slide deck to a public GitHub repository's default branch. | Actual PDF/PPTX binaries, current-revision routing, complete manifests and revision-specific publication evidence. Final remote checks must identify the published commit and file bytes. |

The broader project instructions also ask for a chosen scenario, market/competitor context, reasons for an LLM, security/scalability/efficiency, bias/inaccuracy/cost discussion and persuasive organization. Slides 1-10, 17-20 and the supporting notes address those topics. Slides 15/21 provide labelled economic assumptions; the supplied synthetic example is explicitly generated data. Neither is presented as observed customer performance.

The original starter template was not independently available for verification; the custom deck follows the supplied content criteria without asserting an exact template match.

The later C1-C10 and G1-G8 review lists are useful supplementary checks. They do not add real-world deployment or empirical-business prerequisites to the supplied rubric. Attribution and any later classroom declarations retain their own truthful provenance record in ATTRIBUTION.md.
