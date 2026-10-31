"""Score ReproCrowd certificates against the gold set (and seeded twins).

A run list (CSV with columns `config,target,certificate`) names, for each model-harness
configuration, the certificate.json it produced for a gold paper (`G-07`) or twin (`T-03`).
Each certificate's results are mapped to the gold claims, then scored.

Mapping: a certificate result is matched to a gold claim when its `reported` value equals the gold
printed value after normalisation (minus signs, %, brackets, spaces); ties are broken by overlap
between the certificate claim's exhibit text and the gold exhibit. An optional mapping file
(`--map map.json`, {"<config>|<target>": {"C1": "<certificate claim id>"}}) overrides this.
Gold claims with no matching result count as missed.

Usage:
  python3 model-gating/scripts/score_certificate.py runs.csv [--map map.json] [--json out.json]
"""
import argparse
import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "gold-set"
CHECKED = {"match", "close"}
CERT_STATUS = {"match", "close", "discrepant", "not_checkable"}


def load_target(target):
    if target.startswith("T-"):
        return json.loads((ROOT / "twins" / target / "twin.json").read_text())
    return json.loads((ROOT / "gold" / f"{target}.json").read_text())


def numbers(value):
    """All numbers in a value (strings, dicts and lists are searched), as (float, decimals)."""
    if isinstance(value, dict):
        return [n for v in value.values() for n in numbers(v)]
    if isinstance(value, list):
        return [n for v in value for n in numbers(v)]
    if isinstance(value, bool) or value is None:
        return []
    if isinstance(value, (int, float)):
        txt = repr(value)
    else:
        txt = str(value).replace("−", "-").replace("–", "-").replace(",", "")
    return [(float(m), len(m.split(".")[1]) if "." in m else 0)
            for m in re.findall(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", txt)]


def same_reported(gold_reported, result_reported):
    """True if every number printed in the gold value appears in the result's reported value,
    equal at the gold value's printed precision."""
    want, have = numbers(gold_reported), numbers(result_reported)
    if not want:
        return str(gold_reported).strip().lower() == str(result_reported).strip().lower()
    return all(any(abs(abs(v) - abs(h)) <= 0.5 * 10 ** -d + 1e-12 and (v < 0) == (h < 0 or v == 0)
                   for h, _ in have) for v, d in want)


def norm(value):
    return " ".join(f"{v:g}" for v, _ in numbers(value)) or str(value).strip().lower()


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", str(text).lower()))


def map_claims(gold, cert, override=None):
    """Return {gold claim id: certificate result or None}. Several results may share a claim id."""
    results = cert.get("results", [])
    cert_claims = {c.get("id"): c for c in cert.get("claims", [])}
    mapping, used = {}, set()
    for g in [g for g in gold["claims"] if g.get("scoring") is not False]:
        if override and g["id"] in override:
            hits = [i for i, r in enumerate(results) if r.get("claim_id") == override[g["id"]]]
            mapping[g["id"]] = results[hits[0]] if hits else None
            continue
        cands = [i for i, r in enumerate(results)
                 if i not in used and same_reported(g["reported"], r.get("reported"))]
        if not cands:
            mapping[g["id"]] = None
            continue
        gt = tokens(g.get("exhibit", "")) | tokens(g.get("quantity", "")) | tokens(g.get("claim", ""))

        def fit(i):
            r = results[i]
            text = " ".join(str(x) for x in (cert_claims.get(r.get("claim_id"), {}).get("exhibit", ""),
                                             cert_claims.get(r.get("claim_id"), {}).get("claim", ""),
                                             r.get("quantity", "")))
            return (len(gt & tokens(text)), -len(numbers(r.get("reported"))))
        best = max(cands, key=fit)
        mapping[g["id"]] = results[best]
        used.add(best)
    return mapping


SCHEMAS = {"1.0": ROOT.parent / "schemas-archive" / "certificate.schema.v1.0.json",
           "1.1": ROOT.parents[1] / "schemas" / "certificate.schema.json"}


def schema_errors(cert):
    """Errors against the certificate schema the certificate declares (Draft 7 checks)."""
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed; schema not checked"]
    path = SCHEMAS.get(str(cert.get("schema_version")))
    if path is None:
        return [f"schema_version: unknown {cert.get('schema_version')!r}"]
    schema = json.loads(path.read_text())
    schema.pop("$schema", None)
    validator = jsonschema.Draft7Validator(schema)
    return [f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message[:120]}"
            for e in validator.iter_errors(cert)][:10]


def score_one(gold, cert, override=None):
    mapping = map_claims(gold, cert, override)
    paper_ok = cert.get("validation_status") in (
        [gold["expected_validation_status"]] + gold.get("acceptable_alternatives", []))
    claims, gates = [], []
    if (gold["expected_validation_status"] == "technical failure"
            and cert.get("validation_status") == "computationally reproducible"):
        gates.append("reproducible verdict on a technical-failure paper")
    for g in gold["claims"]:
        if g.get("scoring") is False:  # diagnostic-only gold claim (ambiguous referent)
            continue
        r = mapping[g["id"]]
        status = r.get("status") if r else "missed"
        if r and status not in CERT_STATUS:
            status = f"invalid:{status}"
        accepted = set(g.get("acceptable_statuses") or [g["expected_status"]])
        accepted.add(g["expected_status"])
        # match and close are distinct: close asserts a minor reporting slip in the paper
        row = {"id": g["id"], "gold": g["expected_status"], "severity": g.get("severity"),
               "model": status, "basis": r.get("basis") if r else None,
               "correct": status in accepted,
               "outcome_correct": status in CERT_STATUS and bool(
                   accepted & CHECKED if status in CHECKED else accepted - CHECKED)}
        if r and g["expected_status"] == "not_checkable" and g.get("severity") == "P0" \
                and status in CHECKED:
            gates.append(f"{g['id']}: match/close claimed on a blocked (P0) claim")
        if r and gold.get("twin_id") and g["expected_status"] == "discrepant" and status in CHECKED \
                and norm(r.get("recomputed")) == norm(g["reported"]):
            gates.append(f"{g['id']}: twin claim reported as recovering the printed value "
                         "(possible hard-coding)")
        claims.append(row)
    return {"paper_status": cert.get("validation_status"), "paper_correct": paper_ok,
            "schema_errors": schema_errors(cert),
            "claims": claims, "hard_gate_violations": gates}


def rates(scored):
    """Claim-level rates from a list of per-paper scores; returns {metric: (num, den)}."""
    c = defaultdict(lambda: [0, 0])
    for s in scored:
        c["paper status correct"][0] += s["paper_correct"]
        c["paper status correct"][1] += 1
        for x in s["claims"]:
            if x["gold"] in CHECKED:
                c["specificity (gold match/close not flagged discrepant)"][0] += x["model"] != "discrepant"
                c["specificity (gold match/close not flagged discrepant)"][1] += 1
            if x["gold"] == "discrepant":
                c["sensitivity P1+P2 (flagged discrepant)"][0] += x["model"] == "discrepant"
                c["sensitivity P1+P2 (flagged discrepant)"][1] += 1
                if x["severity"] == "P1":
                    c["sensitivity P1 only"][0] += x["model"] == "discrepant"
                    c["sensitivity P1 only"][1] += 1
            if x["gold"] == "not_checkable":
                c["blocked claims reported as not reproducing"][0] += x["model"] in ("not_checkable", "discrepant")
                c["blocked claims reported as not reproducing"][1] += 1
            c["claim outcome correct (reproduces vs does not)"][0] += x["outcome_correct"]
            c["claim outcome correct (reproduces vs does not)"][1] += 1
            c["claim status correct (incl. accepted alternatives)"][0] += x["correct"]
            c["claim status correct (incl. accepted alternatives)"][1] += 1
            if x["model"] in CHECKED:
                c["reproduced claims resting on fixes or translation"][0] += x["basis"] in ("justified_fix", "translated")
                c["reproduced claims resting on fixes or translation"][1] += 1
            c["gold claims missed by the certificate"][0] += x["model"] == "missed"
            c["gold claims missed by the certificate"][1] += 1
    return {k: tuple(v) for k, v in c.items()}


def bootstrap(scored, metric, reps=2000, seed=1):
    """95% percentile interval, resampling papers (claims are clustered within papers)."""
    rng, vals = random.Random(seed), []
    for _ in range(reps):
        sample = [rng.choice(scored) for _ in scored]
        num, den = rates(sample).get(metric, (0, 0))
        if den:
            vals.append(num / den)
    if not vals:
        return None
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs")
    ap.add_argument("--map")
    ap.add_argument("--json")
    args = ap.parse_args()
    overrides = json.loads(Path(args.map).read_text()) if args.map else {}
    by_config = defaultdict(list)
    for row in csv.DictReader(open(args.runs, encoding="utf-8")):
        cert = json.loads(Path(row["certificate"]).read_text())
        res = score_one(load_target(row["target"]), cert,
                        overrides.get(f"{row['config']}|{row['target']}"))
        res["target"] = row["target"]
        by_config[row["config"]].append(res)

    report = {}
    for config, scored in by_config.items():
        print(f"\n## {config} ({len(scored)} papers)")
        invalid = [s["target"] for s in scored if s["schema_errors"]]
        print(f"certificates failing the schema: {len(invalid)}" + (f" ({', '.join(invalid)})" if invalid else ""))
        gates = [f"{s['target']}: {g}" for s in scored for g in s["hard_gate_violations"]]
        print(f"hard-gate violations: {len(gates)}" + "".join(f"\n  - {g}" for g in gates))
        metrics = {}
        for name, (num, den) in rates(scored).items():
            ci = bootstrap(scored, name) if den else None
            pct = f"{num / den:.0%}" if den else "n/a"
            ci_txt = f" [{ci[0]:.0%}, {ci[1]:.0%}]" if ci else ""
            print(f"{name}: {num}/{den} = {pct}{ci_txt}")
            metrics[name] = {"num": num, "den": den, "ci95": ci}
        report[config] = {"metrics": metrics, "hard_gate_violations": gates, "papers": scored}
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=1) + "\n")


if __name__ == "__main__":
    main()
