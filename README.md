# LineGuide v2.1.0

A hypothetical industrial robot reference advisor for Udacity ND088, Scenario C. Revised 16 November 2026.

Start with the [current PDF](revisions/v2.1.0/artifact/LineGuide_Proposal_v2.1.0.pdf), [editable PowerPoint](revisions/v2.1.0/artifact/LineGuide_Proposal_v2.1.0.pptx) and [revision guide](revisions/v2.1.0/README.md). The [C1-C10 checklist](revisions/v2.1.0/docs/CHECKLIST.md) maps the supplied assessment to specific slides and evidence. The [issue disposition](revisions/v2.1.0/docs/ISSUE-DISPOSITION.md) distinguishes repaired artifact gaps from open deployment and academic requirements.

AI agents contributed substantial product reasoning, architecture, calculations, prose, diagrams and code. Human authorship and verification of every judgment have not been established. The user reported no course-specific permission. This revision makes no own-work or academic-eligibility attestation and has not been submitted in the classroom. See the [current attribution](revisions/v2.1.0/docs/ATTRIBUTION.md) and the [existing policy record](docs/academic-integrity.md).

The current revision supersedes the earlier v2 package's unsupported claims of human-origin reasoning, universal human verification and complete audit closure. Earlier versions remain available as historical records: [v2.0.0](v2-package/README_v2.md), [v1.1.0](submission/LineGuide_Proposal_v1.1.0.pdf) and [v1.0.0](submission/LineGuide_Proposal.pdf). Their dated evidence describes those builds and must not be treated as current proof.

No product deployment, customer interview, model benchmark, measured savings or industrial safety certification is claimed. Scenario facts, proposed settings and unmeasured targets remain separate. The advisor has no robot-control route.

From the clone root:

```sh
python3 revisions/v2.1.0/source/verify.py
/bin/bash tools/extract-audit.sh
```

The first command verifies the complete revision manifest and artifact structure. The extractor reads tracked files and writes an ignored local `audit_bundle.txt`, with every deck labelled by its path. It performs no commit or push. The report includes local Git metadata, so review it before sharing. Artifact checks establish file integrity and documented design coverage; they do not establish an operationally safe product or submission eligibility.
