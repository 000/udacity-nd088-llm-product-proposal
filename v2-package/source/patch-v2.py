#!/usr/bin/env python3
"""Generate deck-content-v2.json from the v1 content with targeted revisions.

Every change is tied to a gate in the external audit (G1-G8) or an Honor Code
control (H1-H4). See docs/CHANGELOG_v2.md for the mapping.
"""
import json, pathlib

here = pathlib.Path(__file__).parent
content = json.loads((here / "deck-content-v1.json").read_text())
slides = content["slides"]

def find(title):
    for s in slides:
        if s.get("title") == title:
            return s
    raise KeyError(title)

# --- Document-level: version marker (supports G1 audit trail) ---
content["version"] = "2.0.0"
content["date"] = "2026-11-16"

# --- R01 limit text: v2 resolves the sampling row with a concrete target (G7) ---
for src in content["sources"]:
    if src["id"] == "R01":
        src["limit"] = ("Documentation verifies supported interfaces, not account entitlement, regional quota, "
                        "measured quality or latency. Proposed limits and sampling settings require endpoint validation. "
                        "Explicit Luna temperature compatibility remains unresolved in vendor docs (feature table vs "
                        "unsupported-parameters section); v2 sets a concrete temperature target of 0.0 with a documented "
                        "fallback to the vendor default if the endpoint rejects the override.")

# --- Cover: versioned meta line (G1) ---
slides[0]["meta"] = "Scenario C \u2022 Udacity ND088\nRevised submission v2 \u2022 16 November 2026"
slides[0]["notes"] += ("\n\nRevision v2 responds to an external evidentiary audit held on 16 November 2026: "
                       "concrete sampling and deployment settings (gate G7), connection-level security callouts on the "
                       "architecture diagram (gate G6), an explicit system-attributes heading (gate G5), and an on-slide "
                       "opportunity-cost statement for the risk gate (gate G4). See README_v2.md and docs/.")

# --- Slide 6 (System attributes, gate G5): explicit heading + primary-goal label ---
s = find("System goals and first-release scope")
s["title"] = "System attributes: goals and pilot scope"
s["leftTitle"] = "Primary system goal"
s["notes"] = ("System attributes required by the rubric: one primary goal and two secondary goals. "
              + s["notes"])

# --- Slide 8 (Architecture, gate G6): enable connection-level security labels ---
s = find("RAG architecture and trust boundaries")
s["seclabels"] = True
s["notes"] = ("Connection-level protections shown on the diagram: device to API uses TLS 1.3 inside an authenticated "
              "Entra session; every back-end link uses a private endpoint with a managed identity; the model endpoint is "
              "reached only inside the approved region or DataZone. "
              + s["notes"])

# --- Slide 10 (LLM configuration, gate G7): concrete deployment model + sampling decision ---
s = find("LLM deployment and configuration")
s["rows"] = [
    ["Deployment model",
     "Cloud on Azure in an approved region or DataZone; private endpoints; no on-prem or edge node needed at 150 queries/day"],
    ["Hosted candidate",
     "Azure OpenAI gpt-6-luna, version 2026-09-22; benchmark before selection"],
    ["Generation",
     "Responses API; reasoning effort low; max_output_tokens 2,000 including reasoning"],
    ["Context budget",
     "System prompt + retrieved context \u22648,000 tokens; visible answer target \u2264800; 15-second deadline"],
    ["Sampling",
     "Temperature 0.0 target for deterministic grounded answers; if the endpoint rejects overrides, accept the vendor "
     "default and record it \u2014 validation gates control residual variance"],
    ["Behavior and tuning",
     "Structured citations + escalation; no fine-tuning or autonomous tool loop"],
]
s["fontSize"] = 21
s["height"] = 476
s["top"] = 150
s["notes"] = ("Concrete settings with justification. Deployment model: cloud (Azure), because the scenario's 150 daily "
              "queries and ten-concurrent-request load need no on-prem or edge capacity; private endpoints and managed "
              "identities keep traffic off the public internet; an approved region or DataZone constrains processing geography. "
              "Sampling: the target is temperature 0.0 because answers are retrieval-grounded explanations where added "
              "sampling variance is risk, not value; Microsoft R01 documentation conflicts on Luna temperature support, so if "
              "the endpoint rejects the override the deployment accepts the vendor default, records it, and relies on the "
              "deterministic guardrails (entitlement filtering, exact catalog matching, citation validation, abstention) to "
              "control residual variance. These are proposed settings, not tested optima. "
              "Candidate: Azure gpt-6-luna version 2026-09-22. Benchmark it and a stronger current model using the same "
              "frozen set; choose the smallest that passes every gate. Account entitlement, regional quota and lifecycle are "
              "unverified. The 2,000-token output cap includes reasoning; target no more than 800 visible tokens. Incomplete "
              "output produces a safe excerpt or escalation, never an unvalidated partial answer. No fine-tuning, persistent "
              "conversation memory, external browsing or autonomous tool loop.")

# --- Slide 12 (Risks, gate G4): on-slide opportunity-cost statement ---
s = find("Five risks and accountable mitigations")
s["caption"] = ("Delay risk: continued search friction and escalation; monetary size unknown \u2014 "
                "bounded discovery limits exposure.")
s["height"] = 428

# --- Slide 19 (sources): updated sampling note (G7) ---
s = find("Sources: system design and privacy")
s["notes"] = ("Microsoft R01 contains contradictory temperature guidance. v2 proposes a concrete temperature target of 0.0 "
              "with a fallback to the vendor default recorded at deployment, resolving the previous sampling row while "
              "preserving the compatibility caveat. Security filtering is application enforced and needs authenticated "
              "server-derived identity. RAG, hybrid search and privacy terms do not establish correct or safe product "
              "behavior. Source claim boundaries and access dates are retained in sources.json.")

out = here / "deck-content.json"
out.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n")
print("wrote", out, "slides:", len(content["slides"]))
