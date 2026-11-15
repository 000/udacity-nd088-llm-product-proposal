#!/usr/bin/env python3
"""Verify this proposal package. No network, credentials or third-party modules."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def close(actual, expected, label):
    assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-7), label


def verify(with_manifest=True):
    checks = []
    assert (ROOT / "VERSION").read_text().strip() == "1.1.0", "version file"
    content = json.loads((ROOT / "source/deck-content.json").read_text())
    assert content.get("version") == "1.1.0", "deck source version"
    metrics = json.loads((ROOT / "docs/metrics.json").read_text())
    rows = metrics["metrics"]
    assert len(rows) == 5, "Exactly five product measurements required"
    assert all(m.get("measured_value") is None for m in rows), "Targets must stay unmeasured"
    checks.append("five proposed KPIs; no fabricated measured values")
    e = metrics["economics"]
    monthly = e["scenario_given_queries_per_day"] * e["assumed_service_days_per_month"]
    close(monthly, 3300, "monthly scenario volume")
    recurring = e["assumed_cloud_allowance_per_month"] + e["assumed_review_hours_per_month"] * e["assumed_review_hourly_cost"]
    close(recurring, 1600, "recurring cost")
    recomputed = []
    for case in e["cases"]:
        n = monthly * case["eligible_share"] * case["adoption_share"] * case["verified_resolution_share"]
        value = n * case["minutes_saved"] / 60 * e["assumed_hourly_capacity_value"]
        net = value - recurring
        close(n, case["successful_sessions"], case["name"] + " sessions")
        close(value, case["capacity_value"], case["name"] + " capacity")
        close(net, case["net_before_implementation"], case["name"] + " net")
        recomputed.append({"case": case["name"], "sessions": round(n, 4), "capacity_usd": round(value, 2), "net_before_implementation_usd": round(net, 2)})
    base = next(c for c in e["cases"] if c["name"] == "base")
    break_even = recurring / base["successful_sessions"] / e["assumed_hourly_capacity_value"] * 60
    close(break_even, e["base_recurring_break_even_minutes_saved"], "break-even minutes")
    close(e["assumed_implementation_labor_cost"] / base["net_before_implementation"], e["base_simple_implementation_payback_months"], "payback")
    envelope = e["pilot_person_weeks"] * e["assumed_cost_per_person_week"] + e["pilot_recurring_months"] * recurring
    close(envelope, 64800, "pilot envelope")
    assert envelope <= e["proposed_pilot_cap"], "envelope exceeds proposed cap"
    checks.append("independently recomputed three economic cases, break-even, payback and pilot envelope")
    sources = json.loads((ROOT / "docs/sources.json").read_text())["sources"]
    ids = [s["id"] for s in sources]
    assert len(ids) == len(set(ids)) == 10, "source IDs"
    assert all(s["url"].startswith("https://") and s["checked_date"] == "2026-11-16" for s in sources)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    config = json.loads((ROOT / "docs/proposed-model-config.json").read_text())
    limits = config["orchestrator_limits"]
    close(sum(limits["input_allocations"].values()), limits["total_input_tokens"], "input allocations")
    close(limits["total_input_tokens"] + limits["max_output_tokens"], limits["input_plus_output_tokens"], "combined token budget")
    assert limits["total_input_tokens"] <= config["documented_vendor_capacity"]["maximum_input_tokens"]
    assert limits["input_plus_output_tokens"] <= config["documented_vendor_capacity"]["context_tokens"]
    assert config["sampling"]["send_temperature"] is False and config["sampling"]["temperature"] is None
    assert config["privacy_proposals"]["offline_private_manual_cache_enabled"] is False
    classroom = json.loads((ROOT / "evidence/v1.1.0/classroom-verification.json").read_text())
    assert classroom["submission_performed"] is False and classroom["confirmation_observed"] is False
    assert classroom["own_work_affirmation_checked"] is False and classroom["eligibility_status"] == "open"
    checks.append("version, complete token allocation, unset temperature and truthful unsubmitted status")
    deck = ROOT / "submission/LineGuide_Proposal_v1.1.0.pptx"
    with zipfile.ZipFile(deck) as z:
        assert z.testzip() is None, "corrupt PPTX member"
        slide_paths = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)))
        assert len(slide_paths) == len(content["slides"]) == 25, "unexpected slide count"
        texts = [" ".join(t.text or "" for t in ET.fromstring(z.read(n)).findall(".//a:t", ns)) for n in slide_paths]
        notes = [n for n in z.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)]
        assert len(notes) == len(slide_paths), "missing slide notes"
        combined = "\n".join(texts) + "\n" + "\n".join(z.read(n).decode() for n in notes)
        assert "LineGuide" in combined and "Scenario C" in combined
        for source_id in ids:
            assert source_id in combined, "uncited source: " + source_id
        assert "1.1.0" in combined, "missing visible version"
        components = json.loads((ROOT / "docs/components.json").read_text())["components"]
        assert len(components) == 10
        normalized = re.sub(r"\s+", " ", combined)
        for item in components:
            assert re.search(r"\b" + re.escape(item["id"]) + r"\s+" + re.escape(item["label"]) + r"\b", normalized), "missing component label: " + item["id"]
        assert "/Users/" not in combined, "private account path in deck"
        checks.append("PPTX ZIP integrity, slide/notes count and all ten source IDs")
    pdf = (ROOT / "submission/LineGuide_Proposal_v1.1.0.pdf").read_bytes()
    assert pdf.startswith(b"%PDF-"), "invalid PDF header"
    checks.append("PDF file header; rendered review is recorded separately")
    text_suffixes = {".md", ".json", ".py", ".mjs", ".mmd", ".txt"}
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in text_suffixes:
            content = p.read_text()
            # This verifier necessarily contains the pattern it checks.
            assert not re.search(r"/Users/[A-Za-z0-9_.-]+/", content), "private account path: " + str(p.relative_to(ROOT))
            assert "-----BEGIN " + "PRIVATE KEY-----" not in content, "private key pattern"
    checks.append("bounded public-text account-path and private-key screening")
    legacy = {"LineGuide_Proposal.pptx": "6abc0af75c5bfc2c86f7e040e9a162d593620ed32b83acf34ff86ce844e13f86", "LineGuide_Proposal.pdf": "e6243d6771135ba4324f1b65db94c3fe526deded8fedc5c800ea4562537e98c3"}
    for name, digest in legacy.items():
        assert hashlib.sha256((ROOT / "submission" / name).read_bytes()).hexdigest() == digest, "legacy artifact changed"
    for p in ROOT.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            assert not p.read_bytes().startswith(b"version https://git-lfs.github.com/spec/v1"), "LFS pointer: " + str(p.relative_to(ROOT))
    bundle = ROOT / "submission/LineGuide_v1.1.0_review_bundle.zip"
    if bundle.exists():
        with zipfile.ZipFile(bundle) as z:
            assert z.testzip() is None, "review bundle CRC"
            assert "SHA256SUMS" in z.namelist() and "README.md" in z.namelist()
            for name in ["submission/LineGuide_Proposal_v1.1.0.pptx", "submission/LineGuide_Proposal_v1.1.0.pdf"]:
                assert z.read(name) == (ROOT / name).read_bytes(), "bundle artifact mismatch: " + name
    checks.append("original exports preserved, no Git LFS pointers and review-bundle artifact integrity when present")
    count = None
    if with_manifest:
        manifest = ROOT / "SHA256SUMS"
        entries = []
        for line in manifest.read_text().splitlines():
            digest, rel = line.split("  ", 1)
            path = ROOT / rel
            assert path.resolve().is_relative_to(ROOT), "manifest path escapes package"
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, "hash mismatch: " + rel
            entries.append(rel)
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and p.name != "SHA256SUMS" and "__pycache__" not in p.parts}
        assert set(entries) == actual and len(entries) == len(actual), "manifest coverage mismatch"
        count = len(entries)
        checks.append("SHA-256 of every published file except the manifest itself")
    return {"status": "passed", "scope": "artifact checks; no operational advisor tested", "checks": checks, "manifest_files_checked": count, "slides": len(slide_paths), "speaker_notes": len(notes), "economics": recomputed}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--without-manifest", action="store_true", help="structural preflight before manifest creation")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(not args.without_manifest), indent=2))
    except (AssertionError, OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}))
        sys.exit(1)
