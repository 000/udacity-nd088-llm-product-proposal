# LineGuide v2.3.0

A completed hypothetical product proposal for Udacity ND088, Scenario C. [CURRENT.json](CURRENT.json) identifies the sole current package.

Open the [PDF](revisions/v2.3.0/artifact/LineGuide_Proposal_v2.3.0.pdf), [editable PowerPoint](revisions/v2.3.0/artifact/LineGuide_Proposal_v2.3.0.pptx), or [self-contained review ZIP](review/LineGuide_Review_v2.3.0.zip). The ZIP contains the actual deck, complete text and notes, standalone diagrams with Mermaid source, supporting documents, reproducible simulation and checksums.

The [actual rubric map](revisions/v2.3.0/docs/RUBRIC-MAP.md) covers the problem, solution, risks, system goals, architecture, LLM settings and success measurements, plus default-branch packaging. The supplied assignment asks for a hypothetical product plan; it does not require an operating business, real customer telemetry or completed product experiments.

Scenario facts, planning assumptions and synthetic results are labelled separately. The supplied generator reproduces its advertised dataset hash; its outputs illustrate the case without being presented as real customer measurements. See the [simulation audit](revisions/v2.3.0/docs/SYNTHETIC-BASELINE-AUDIT.md). Evaluation and rollout describe future implementation work.

The deck has a 16-slide decision narrative and eight appendices. AI assistance is documented accurately in [ATTRIBUTION.md](revisions/v2.3.0/docs/ATTRIBUTION.md). Publication is separate from classroom submission; no submission or own-work attestation was performed.

From the clone root:

```sh
python3 verify.py
/bin/bash tools/extract-audit.sh
```

The verifier follows `CURRENT.json`. The extractor labels every repository deck and writes an ignored local `audit_bundle.txt`. [Publication evidence](review/PUBLICATION.json) identifies the verified artifact commit and hashes. Earlier versions remain in [version history](ARCHIVE.md).
