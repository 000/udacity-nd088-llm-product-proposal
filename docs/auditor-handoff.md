# Audit handoff

An assessor who cannot retrieve repository URLs should receive `LineGuide_v1.1.0_review_bundle.zip`, or at minimum the v1.1.0 PDF, PPTX, README and manifest. The ZIP contains the actual exports, notes in the PPTX, source content, configuration, references and evidence records. It carries its own `SHA256SUMS`; the repository manifest separately binds the ZIP itself. Neither manifest includes its own hash.

Extract the bundle into a clean directory and run `python3 source/verify.py` there. For the repository, run the same command from its root. A successful result establishes the listed file/structure/arithmetic properties. Inspect the PDF visually and read the notes before judging coverage; a hash match alone does not evaluate a proposal.

The baseline commit/tree and full file inventory are under `evidence/v1.1.0/`. They record an actual fetch at the specified commit. Current versioned files and GitHub history identify the revised publication. The original unversioned PDF/PPTX are v1.0.0, not the current candidate. The archived verifier describes that older snapshot and is not the current verification entry point.

Read the revision response and academic-integrity record before interpreting a content review as permission to submit. Academic eligibility remains open and the classroom was left unsubmitted. The template resource was identified but not retrieved successfully, so exhaustive template matching was not checked. No external assessor verdict, plagiarism clearance, student-authorship certification or Udacity grade is asserted.
