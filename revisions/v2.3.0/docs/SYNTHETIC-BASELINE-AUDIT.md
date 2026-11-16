# Supplied synthetic baseline audit

Revision 2.3.0, 16 November 2026. The later attachment supplies several code variants and a final fixed-seed simulation. It explicitly states that no proprietary logs, customer data or real PII underlie the results. It therefore supplies a reproducible methods example for the hypothetical proposal. The supplied rubric does not require real customer measurements.

## Reproduction

The final generator was inspected before execution. Its unused SciPy import was removed because SciPy was unavailable; no parameter, seed, draw order or generated value changed. The original selected code is identified by hash in the verification record. The published generator requires NumPy and pandas; the standard-library artifact verifier remains separate.

The canonical six-decimal CSV reproduces the advertised SHA-256:

```text
cef03be7adb723bab005ea3d5ab679c3f418910d5f2612f5f7eccd74c9013de2
```

| Reproduced simulation quantity | Result |
| --- | --- |
| Generated sessions / timed sample | 1,500 / 240 |
| Generated outcomes | 485 resolved, 605 escalated, 410 abandoned/workaround |
| Mean sampled search time | 22.8153776071 minutes |
| Mean generated support handling time | 29.6086305292 minutes |

The [verification record](../evidence/synthetic-baseline-check.json) records runtime versions, arithmetic and uncertainty scope. The [simulation directory](../simulation/) contains the explicitly synthetic CSV and metadata; [source/synthetic-baseline.py](../source/synthetic-baseline.py) reproduces it. Earlier code variants in the attachment use different parameters and produce different figures; they must not be mixed with this final dataset.

## Corrections and interpretation

- **Provenance:** Generated tickets are a complete enumeration of a simulated frame. They are not CRM telemetry, de-identified employee records or observations of 48 technicians. The final schema contains no technician identifier; those claimed identifiers cannot be inferred from it.
- **Cost:** Use arithmetic means for aggregate hours, keep customer search labor separate from OEM support labor, and disclose the assumed hourly rates. The attachment's BLS/industry anchors have not been independently established here. The proposed US/global rates are sensitivity assumptions. Languages do not establish where a workforce lives or its wage mix. The combined amount is an ecosystem illustration, not one firm's P&L, avoidable cash cost or realized savings.
- **Sampling:** The generated 15-stratum frame has proportional 16% sampling. The factor 0.84 applies to variance; its standard-error multiplier is the square root of 0.84. A statement about 375 topic/model combinations requires evidence that those cells actually exist; the supplied five-domain/three-family aggregation is an invented simulation taxonomy.
- **Intervals:** Any sampling interval describes the specified artificial sampling design. Wilson calculations for all generated outcomes are not confidence intervals for a live customer population. They do not establish real-world precision, effect size or safety.
- **Language effects:** Resolution and duration penalties are coded into the generator. Their resulting gaps cannot demonstrate a causal effect of the English-only knowledgebase or predict actual language-group performance.
- **Claims:** “Signed,” “verified to the cent” and excluded-downtime statements do not establish human approval or a conservative bound on real costs. Generated outcomes do not prove demand, an LLM's incremental benefit, implementation feasibility or industrial safety.

The real-data [baseline template](baseline-template.csv) remains empty and separate. The [discovery protocol](EMPIRICAL-EVIDENCE.md) still governs collection. The deck labels the simulation and planning assumptions explicitly. No real business or field study is required to produce the course proposal; a future implementation would validate those assumptions.
