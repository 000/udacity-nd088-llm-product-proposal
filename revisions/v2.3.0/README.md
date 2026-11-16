# LineGuide revision 2.3.0

LineGuide is a product proposal for Udacity ND088's hypothetical Scenario C: an LLM-powered industrial robot expert advisor. The deck defines the customer problem, product benefits, risks, system design, model configuration and success measurements. Scenario facts, planning assumptions and synthetic examples are labelled separately.

Open the [PDF](artifact/LineGuide_Proposal_v2.3.0.pdf) or [editable PowerPoint](artifact/LineGuide_Proposal_v2.3.0.pptx). Slides 1-16 form the stakeholder narrative; slides 17-24 provide supporting technical, scenario, economic and attribution detail. The [actual rubric map](docs/RUBRIC-MAP.md) identifies the seven supplied grading criteria and public/default-branch packaging requirement. The [checklist](docs/CHECKLIST.md) records the corresponding artifact checks without promising a grade.

## Review without the GitHub page

The [self-contained review bundle](../../review/LineGuide_Review_v2.3.0.zip) includes the actual deck files, [complete slide text and notes](slides-and-notes.md), [standalone diagrams and Mermaid source](diagrams/), supporting documents, scoped repository metadata/tree and file hashes. Reviewers can inspect the materials without retrieving GitHub's repository page. An empty HTML shell does not establish that a repository is private.

From this package directory:

```sh
shasum -a 256 -c SHA256SUMS
```

From the repository root, the version-controlled extractor writes an ignored local report and labels every current or historical deck by path:

```sh
/bin/bash tools/extract-audit.sh
```

This revision is the current candidate; earlier packages remain history. The [assessment response](docs/REVIEW-RESPONSE.md) explains the changes. The [reproduced synthetic example](docs/SYNTHETIC-BASELINE-AUDIT.md) and [methods note](docs/EMPIRICAL-EVIDENCE.md) support the illustrative business analysis. Real customer measurements, live model calls and production approvals are future implementation work, not requirements for completing this hypothetical proposal.

The [attribution](docs/ATTRIBUTION.md) records substantive AI assistance and the limits of human-review evidence. No own-work attestation, classroom submission or industrial safety certification is claimed. Export, visual, checksum, bundle and publication outcomes belong in the revision's [evidence records](evidence/); those records must reflect the final files after the latest edits.
