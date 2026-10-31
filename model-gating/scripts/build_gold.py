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
GOLD_VERSION = "1.2"
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
            merged.append(entry)
        alts = sorted(set(sol["acceptable_alternatives"]) | set(EXTRA_ALTERNATIVES.get(gid, [])))
        conf = min(sol["label_confidence"], cla["label_confidence"], key=CONF.index)
        record = {
            "gold_id": gid, "gold_version": GOLD_VERSION, "cand_id": claims["cand_id"],
            "doi": claims["doi"], "title": claims["title"], "stratum_drawn": claims["stratum_drawn"],
            "paper_url": claims["paper_url"], "package": claims["package"],
            "source_evidence": claims["source_evidence"],
            "expected_validation_status": sol["expected_validation_status"],
            "acceptable_alternatives": alts, "label_confidence": conf,
            "requires_human_rerun": sol.get("requires_human_rerun") or cla.get("requires_human_rerun") or None,
            "corrections": sol.get("corrections", []) + [c for c in cla.get("corrections", [])
                                                         if c not in sol.get("corrections", [])]
                           + ([V12_NOTE] if any(g == gid for g, _ in DROP_STATUSES) else []),
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
