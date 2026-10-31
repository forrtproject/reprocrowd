"""Sanity tests for score_certificate.py using synthetic certificates built from the gold set.

- oracle: reports every gold status and paper verdict; must score 100% with no gate violations.
- oracle_renumbered: the same, with shuffled order and different claim ids; mapping must still work.
- naive_all_match: claims every value matches and every paper reproduces; must fail sensitivity,
  abstention and the technical-failure gate.
Run: python3 model-gating/scripts/test_score_certificate.py
"""
import csv
import json
import random
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score_certificate as sc  # noqa: E402


def make_cert(gold, mode, rng):
    claims, results = [], []
    order = list(gold["claims"])
    if mode == "oracle_renumbered":
        rng.shuffle(order)
    for i, g in enumerate(order, 1):
        cid = f"C{i + 40}" if mode == "oracle_renumbered" else g["id"]
        claims.append({"id": cid, "claim": g.get("claim", ""), "exhibit": g.get("exhibit", "")})
        status = "match" if mode == "naive_all_match" else g["expected_status"]
        results.append({"claim_id": cid, "quantity": g.get("quantity", ""),
                        "reported": g["reported"],
                        "recomputed": g.get("reference_recomputed") or g["reported"],
                        "status": status})
    verdict = ("computationally reproducible" if mode == "naive_all_match"
               else gold["expected_validation_status"])
    return {"claims": claims, "results": results, "validation_status": verdict}


def main():
    rng = random.Random(7)
    golds = sorted((sc.ROOT / "gold").glob("G-*.json"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        runs = []
        for mode in ["oracle", "oracle_renumbered", "naive_all_match"]:
            for p in golds:
                gold = json.loads(p.read_text())
                path = tmp / f"{mode}_{p.stem}.json"
                path.write_text(json.dumps(make_cert(gold, mode, rng)))
                runs.append({"config": mode, "target": p.stem, "certificate": str(path)})
        scored = {}
        for r in runs:
            res = sc.score_one(sc.load_target(r["target"]), json.loads(Path(r["certificate"]).read_text()))
            scored.setdefault(r["config"], []).append(res)
    for mode in ["oracle", "oracle_renumbered"]:
        m = sc.rates(scored[mode])
        assert all(s["hard_gate_violations"] == [] for s in scored[mode]), mode
        assert m["claim status correct (incl. accepted alternatives)"][0] == \
            m["claim status correct (incl. accepted alternatives)"][1], (mode, m)
        assert m["gold claims missed by the certificate"][0] == 0, (mode, m)
        assert m["paper status correct"] == (30, 30), (mode, m)
    m = sc.rates(scored["naive_all_match"])
    assert m["sensitivity P1+P2 (flagged discrepant)"][0] == 0
    assert m["abstention (gold not_checkable reported not_checkable)"][0] == 0
    gates = [g for s in scored["naive_all_match"] for g in s["hard_gate_violations"]]
    assert any("technical-failure" in g for g in gates)
    print("all tests passed;", {k: f"{v[0]}/{v[1]}" for k, v in m.items()})


if __name__ == "__main__":
    main()
