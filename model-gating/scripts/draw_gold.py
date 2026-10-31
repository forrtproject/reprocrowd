"""Stratified random draw of the 30-paper gold set from the screened candidate pool.

Within each stratum, eligible high-confidence candidates are drawn first, then medium, then low,
each tier shuffled with a fixed seed. Candidates with code embedded in a PDF/HTML are capped.
Usage: python3 model-gating/scripts/draw_gold.py [--quota reproducible=10,...]
"""
import argparse
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gold-set"
SEED = 20261030
QUOTA = {
    "computationally reproducible": 10,
    "computational issues": 10,
    "technical failure": 5,
    "ambiguous": 5,
}
TIERS = ["high", "medium", "low"]
EMBEDDED_CAP = 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quota", help="override, e.g. 'technical failure=4,computational issues=11'")
    args = ap.parse_args()
    quota = dict(QUOTA)
    if args.quota:
        for part in args.quota.split(","):
            k, v = part.rsplit("=", 1)
            quota[k.strip()] = int(v)

    rows = list(csv.DictReader(open(ROOT / "candidates.csv", encoding="utf-8")))
    pool = [r for r in rows if r["eligible"] == "true" and r["language_ok"] == "true"]
    rng = random.Random(SEED)
    drawn, reserve, embedded = [], {}, 0
    for stratum, n in quota.items():
        cands = [r for r in pool if r["provisional_stratum"] == stratum]
        ordered = []
        for tier in TIERS:
            tier_rows = sorted((r for r in cands if r["screener_confidence"] == tier),
                               key=lambda r: r["cand_id"])
            rng.shuffle(tier_rows)
            ordered += tier_rows
        picked = []
        for r in ordered:
            if len(picked) == n:
                break
            is_embedded = "code_format=embedded" in r["notes"]
            if is_embedded and embedded >= EMBEDDED_CAP:
                continue
            embedded += is_embedded
            picked.append(r)
        if len(picked) < n:
            print(f"WARNING: {stratum}: only {len(picked)} of {n} available")
        drawn += picked
        reserve[stratum] = [r["cand_id"] for r in ordered if r not in picked]

    out = {
        "seed": SEED,
        "quota": quota,
        "drawn": [
            {"gold_id": f"G-{i + 1:02d}", "cand_id": r["cand_id"],
             "stratum": r["provisional_stratum"], "title": r["title"], "doi": r["doi"]}
            for i, r in enumerate(drawn)
        ],
        "reserve_in_draw_order": reserve,
    }
    (ROOT / "draw.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for d in out["drawn"]:
        print(d["gold_id"], d["cand_id"], d["stratum"], "|", d["title"][:70])


if __name__ == "__main__":
    main()
