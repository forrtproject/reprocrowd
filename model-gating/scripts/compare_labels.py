"""Compare two labellers' independent gold labels and list every disagreement.

Each labeller writes gold-set/labels/<labeller>/<gold_id>.json with:
  {"gold_id", "expected_validation_status", "acceptable_alternatives": [...],
   "claims": [{"id", "expected_status", "reference_recomputed", "severity", "rationale"}],
   "label_confidence"}
Claim ids come from the shared claim list (gold-set/claims/<gold_id>.json).
Usage: python3 model-gating/scripts/compare_labels.py sol claude
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gold-set"


def num(x):
    try:
        return float(str(x).replace("−", "-").replace(",", ""))
    except (TypeError, ValueError):
        return None


def same_value(a, b):
    na, nb = num(a), num(b)
    if na is not None and nb is not None:
        return abs(na - nb) <= 1e-9 + 0.005 * max(abs(na), abs(nb))
    return str(a).strip().lower() == str(b).strip().lower()


def main(a, b):
    da, db = ROOT / "labels" / a, ROOT / "labels" / b
    ids = sorted({p.stem for p in da.glob("G-*.json")} | {p.stem for p in db.glob("G-*.json")})
    n_claims = n_status_agree = n_paper_agree = 0
    report = []
    for gid in ids:
        pa, pb = da / f"{gid}.json", db / f"{gid}.json"
        if not (pa.exists() and pb.exists()):
            report.append(f"{gid}: missing from {'b' if pa.exists() else 'a'}")
            continue
        la, lb = json.loads(pa.read_text()), json.loads(pb.read_text())
        if la["expected_validation_status"] == lb["expected_validation_status"]:
            n_paper_agree += 1
        else:
            report.append(f"{gid}: PAPER {a}={la['expected_validation_status']} "
                          f"{b}={lb['expected_validation_status']}")
        ca = {c["id"]: c for c in la["claims"]}
        cb = {c["id"]: c for c in lb["claims"]}
        for cid in sorted(set(ca) | set(cb)):
            if cid not in ca or cid not in cb:
                report.append(f"{gid} {cid}: labelled by only one")
                continue
            x, y = ca[cid], cb[cid]
            n_claims += 1
            diffs = []
            if x["expected_status"] == y["expected_status"]:
                n_status_agree += 1
            else:
                diffs.append(f"status {x['expected_status']} vs {y['expected_status']}")
            if (x.get("severity") or None) != (y.get("severity") or None):
                diffs.append(f"severity {x.get('severity')} vs {y.get('severity')}")
            if not same_value(x.get("reference_recomputed"), y.get("reference_recomputed")):
                diffs.append(f"ref {x.get('reference_recomputed')} vs {y.get('reference_recomputed')}")
            if diffs:
                report.append(f"{gid} {cid}: " + "; ".join(diffs))
    print(f"papers compared: {len(ids)}; paper status agreement {n_paper_agree}/{len(ids)}")
    print(f"claims compared: {n_claims}; claim status agreement {n_status_agree}/{n_claims}")
    print("\n".join(report) if report else "no disagreements")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
