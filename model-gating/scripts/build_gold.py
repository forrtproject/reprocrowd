"""Merge the shared claim lists and the reconciled labels into the gold records.

Inputs: gold-set/claims/G-xx.json, gold-set/labels/sol/ and labels/claude/ (reconciled; statuses and
severities must agree). Sol's labels carry the curated references and diagnostics (rule R5).
Paper-level alternatives follow rule R7 (see reconciliation.md); confidence is the lower of the two.
Writes gold-set/gold/G-xx.json and gold-set/gold-summary.csv.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gold-set"
GOLD_VERSION = "1.3"
CONF = ["low", "medium", "high"]
# R7: paper-level alternatives only at category boundaries (lossless-edit, version/stochastic noise)
EXTRA_ALTERNATIVES = {"G-11": ["computational issues"], "G-19": ["computational issues"]}
# v1.2: match and close are distinct outcomes (close asserts a minor reporting slip), so a claim
# never accepts both. Only G-08 C4 did; its printed 0.19 is a truncation of 0.198, so close stands.
DROP_STATUSES = {("G-08", "C4"): ["match"]}
V12_NOTE = {"version": "1.2", "change": "C4 no longer accepts match; close only.",
            "reason": "From v1.2, match and close are distinct: close asserts a minor reporting slip "
                      "(printed 0.19 truncates 0.198). Decision by Lukas Wallrich, 31 Oct 2026.",
            "evidence": "C4 reference_recomputed 0.198 (I4R report, section 3)"}
# v1.3 (review rounds 5 and 6, audit/v1.3/): G-08 rereading and rule R10 for the close boundary.
G11_LOG = ("https://huggingface.co/datasets/chuxuan/REPRO-Bench/resolve/74958fba32daeacff51f2e1fd37be3916595648f/"
           "29/replication_package/Code/LOG/log_Table%201%2C%20SI3%2C%20SI4%2C%20SI5%2C%20Figure%20SI13%2C%20SI14.txt")
R10 = "R10 (audit/v1.3/sol-review-r10.md)"


def to_close(slip):
    return {"expected_status": "close", "severity": None, "acceptable_statuses": ["close"],
            "r10_slip_evidence": slip}


def g11_match(value, line, report_value):
    return {"expected_status": "match", "severity": None, "acceptable_statuses": ["match"],
            "reference_recomputed": value, "reference_provenance": "shipped_output",
            "reference_evidence": f"{G11_LOG} line {line} (treatBin); generated Table 1 row, line 485",
            "diagnostic_results": [{"value": report_value, "provenance": "source_report",
                                    "evidence": "I4R-DP036 Table 1", "is_scoring_reference": False,
                                    "scope": "Report-run value; cause of the difference from the "
                                             "authors' log is unresolved."}]}


V13_CLAIMS = {
    ("G-08", "C6"): {
        "claim": "Museum visit and support for pardoning perpetrators: the follow-up estimate the "
                 "durability paragraph reports as no longer significant",
        "expected_status": "match", "severity": None, "acceptable_statuses": ["match"],
        "reference_recomputed": 0.2047054162220282, "reference_recomputed_p": 0.1640234163763856,
        "reference_provenance": "agent_rerun", "reference_scope": "24-week follow-up (week 1: 0.308, "
        "p = .004; week 8: 0.243, p = .048); the paragraph leaves the wave implicit",
        "reference_evidence": "audit/v1.3/g08_check.R and g08_check.log; audit/v1.3/sol-review.md"},
    ("G-08", "C7"): {
        "expected_status": "not_checkable", "severity": None, "acceptable_statuses": ["not_checkable"],
        "scoring": False, "reference_recomputed": None,
        "reference_scope": "Denominator unverifiable: 18/137 = 13.14% (printed), 18/135 = 13.33% "
        "(valid responses), 18/138 = 13.04% (treated). Diagnostic only; excluded from scoring.",
        "reference_evidence": "audit/v1.3/g08_check.log; audit/v1.3/sol-review.md"},
    ("G-11", "C2"): g11_match(-1.06359, 224, -1.066),
    ("G-11", "C5"): g11_match(-0.569135, 373, -0.574),
    ("G-18", "C1"): to_close("Partial eta-squared .004 printed as .01; the two main-effect effect sizes "
                             "appear transposed (.012 and .004 vs printed .01 and < .01)."),
    ("G-22", "C1"): to_close("Source report identifies truncation: .07849 printed as .07."),
    ("G-22", "C2"): to_close("Source report lists the intercept 5.25 vs 5.28 among the table's typos."),
    ("G-22", "C3"): to_close("Source report contrasts [5.08, 5.43] with [5.11, 5.44] in the intercept-typo "
                             "discussion; both endpoints within 1%."),
}
V13_PAPERS = {"G-08": "computationally reproducible"}
V13_NOTES = {
    "G-08": {"version": "1.3", "change": "C6 discrepant -> match (24-week estimate); C7 discrepant -> "
             "non-scoring diagnostic; paper computational issues -> computationally reproducible.",
             "reason": "Round 4 misattributed b = 0.20, p = .16 to week 1; the paragraph leaves the wave "
                       "implicit and the pair is exactly the 24-week estimate. 13.14% = 18/137 with an "
                       "unverifiable denominator. Agreed by Sol, round 5.",
             "evidence": "audit/v1.3/g08_check.log; audit/v1.3/sol-review.md"},
    "G-11": {"version": "1.3", "change": "C2, C5 close -> match with shipped-log references.",
             "reason": f"Authors' pinned log gives -1.063590 and -0.569135; {R10}.",
             "evidence": G11_LOG},
    "G-18": {"version": "1.3", "change": "C1 discrepant -> close (named slip).", "reason": R10,
             "evidence": "audit/v1.3/sol-review-r10.md"},
    "G-22": {"version": "1.3", "change": "C1-C3 discrepant -> close (source-identified typos).",
             "reason": R10, "evidence": "audit/v1.3/sol-review-r10.md"},
}
# v1.0 flagged G-04 and G-26 for a human rerun; from v1.1 the flag comes from the label files.


def main():
    out_dir = ROOT / "gold"
    out_dir.mkdir(exist_ok=True)
    rows = []
    for cpath in sorted((ROOT / "claims").glob("G-*.json")):
        gid = cpath.stem
        claims = json.loads(cpath.read_text())
        sol = json.loads((ROOT / "labels" / "sol" / f"{gid}.json").read_text())
        cla = json.loads((ROOT / "labels" / "claude" / f"{gid}.json").read_text())
        assert sol["expected_validation_status"] == cla["expected_validation_status"], gid
        cla_claims = {c["id"]: c for c in cla["claims"]}
        merged = []
        for c in claims["claims"]:
            s, k = next(x for x in sol["claims"] if x["id"] == c["id"]), cla_claims[c["id"]]
            assert s["expected_status"] == k["expected_status"], (gid, c["id"])
            assert (s.get("severity") or None) == (k.get("severity") or None), (gid, c["id"])
            entry = {**c, **{x: v for x, v in s.items() if x != "id"}}
            entry["acceptable_statuses"] = sorted(
                (set(s.get("acceptable_statuses") or []) | set(k.get("acceptable_statuses") or [])
                 | {s["expected_status"]}) - set(DROP_STATUSES.get((gid, c["id"]), [])))
            entry["second_labeller_rationale"] = k.get("rationale", "")
            entry.update(V13_CLAIMS.get((gid, c["id"]), {}))
            merged.append(entry)
        alts = sorted(set(sol["acceptable_alternatives"]) | set(EXTRA_ALTERNATIVES.get(gid, [])))
        conf = min(sol["label_confidence"], cla["label_confidence"], key=CONF.index)
        record = {
            "gold_id": gid, "gold_version": GOLD_VERSION, "cand_id": claims["cand_id"],
            "doi": claims["doi"], "title": claims["title"], "stratum_drawn": claims["stratum_drawn"],
            "paper_url": claims["paper_url"], "package": claims["package"],
            "source_evidence": claims["source_evidence"],
            "expected_validation_status": V13_PAPERS.get(gid, sol["expected_validation_status"]),
            "acceptable_alternatives": alts, "label_confidence": conf,
            "requires_human_rerun": sol.get("requires_human_rerun") or cla.get("requires_human_rerun") or None,
            "corrections": sol.get("corrections", []) + [c for c in cla.get("corrections", [])
                                                         if c not in sol.get("corrections", [])]
                           + ([V12_NOTE] if any(g == gid for g, _ in DROP_STATUSES) else [])
                           + ([V13_NOTES[gid]] if gid in V13_NOTES else []),
            "labelled_by": ["gpt-6.1-sol", "claude-opus-5-5"],
            "claims": merged,
            "notes": {"claim_list": claims.get("notes", ""), "sol": sol.get("notes", ""),
                      "claude": cla.get("notes", ""),
                      "claude_blind_original_historical": cla.get("notes_blind_original", "")},
        }
        (out_dir / f"{gid}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
        statuses = [c["expected_status"] for c in merged]
        rows.append({
            "gold_id": gid, "cand_id": claims["cand_id"], "doi": claims["doi"],
            "title": claims["title"], "stratum_drawn": claims["stratum_drawn"],
            "expected_validation_status": record["expected_validation_status"],
            "acceptable_alternatives": "; ".join(alts), "n_claims": len(merged),
            **{f"n_{s}": statuses.count(s) for s in ["match", "close", "discrepant", "not_checkable"]},
            "severities": "; ".join(sorted({c["severity"] for c in merged if c.get("severity")})),
            "label_confidence": conf, "requires_human_rerun": bool(record["requires_human_rerun"]),
        })
    with open(ROOT / "gold-summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} gold records")


if __name__ == "__main__":
    main()
