"""Run benchmark targets (gold papers G-xx, twins T-xx) with one Codex CLI configuration.

Each run gets a fresh directory outside the repository (no gold, labels or twin metadata in
reach) and the benchmark prompt with the article DOI and code link filled in. Twins get a local
package rebuilt by build_twin_package.py. Certificates are copied back into
model-gating/benchmark/runs/<config>/ and listed in runs-<config>.csv for score_certificate.py.

Stata papers (S-xx, ../gold-set/stata/draw-stata.json) get the local package built by
build_stata_packages.py and, as they have no gold claim list yet, an instruction to extract and
check every reported number.

Each run installs R packages into its own library, layered over the shared one, so parallel runs
cannot change each other's packages.

Usage:
  python3 model-gating/benchmark/run_codex.py --config luna --model gpt-6-luna \
      --effort medium --jobs 3 G-08 G-21 T-02
Reruns skip targets whose certificate was already collected (delete it to rerun).
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GOLD = HERE.parent / "gold-set"
WORK = Path("/tmp/scratch_bench_luna")
LOCAL_NOTE = ("(a local copy of the shipped code and data; treat this folder as the package and do "
              "not download another copy)")
STATA_CLAIMS = (
    "No claim list is given for this paper. Number your own claims C1, C2, and so on. Extract "
    "every number in the article's abstract, main text and tables that reports a result computed "
    "from the data (estimates, standard errors, test statistics, p values, intervals, sample sizes, "
    "descriptive statistics), and check each one. The analysis code is in Stata, and Stata is not "
    "installed: translate it command by command into R, keep the translation under code/, and mark "
    "those results basis: translated. Translate the whole shipped pipeline, data preparation as well "
    "as analysis, not only the parts behind one table or figure. Nothing requires you to stop early: "
    "report a result as not_checkable only when the shipped code or data cannot produce it, never "
    "because translating it would take long.")


def claim_block(gold_id):
    """The verdict-free claim list (claims/G-xx.json): ids, wording, location and printed values."""
    gold = {c["id"]: c for c in json.loads((GOLD / "gold" / f"{gold_id}.json").read_text())["claims"]}
    lines = []
    for c in json.loads((GOLD / "claims" / f"{gold_id}.json").read_text())["claims"]:
        if gold.get(c["id"], {}).get("scoring") is False:
            continue
        printed = c["reported"] + (f" (p = {c['reported_p']})" if c.get("reported_p") else "")
        page = f", p. {c['page']}" if c.get("page") else ""
        lines.append(f"- {c['id']}: {c['claim']} ({c['exhibit']}{page}). "
                     f"{c.get('quantity') or 'Value'} printed as {printed}.")
    return "\n".join(lines)


def target_info(target):
    if target.startswith("S-"):
        from build_stata_packages import opaque
        draw = json.loads((GOLD / "stata" / "draw-stata.json").read_text())
        entry = next(e for e in draw["drawn"] if e["stata_id"] == target)
        pkg = WORK / "packages" / opaque(target, draw["seed"])
        if not pkg.exists():
            raise SystemExit(f"{target}: build the package first (build_stata_packages.py)")
        article = WORK / "articles" / pkg.name / "article.pdf"
        doi = entry["doi"] + (f" (a copy of the published article is at {article}; read the printed "
                              "values from it)" if article.exists() else "")
        return doi, f"{pkg} {LOCAL_NOTE}", STATA_CLAIMS
    if target.startswith("T-"):
        twin = json.loads((GOLD / "twins" / target / "twin.json").read_text())
        gold = json.loads((GOLD / "gold" / f"{twin['base_gold_id']}.json").read_text())
        pkg = WORK / "packages" / target
        if not pkg.exists():
            subprocess.run([sys.executable, str(HERE / "build_twin_package.py"), target, str(pkg)],
                           check=True)
        link = f"{pkg} {LOCAL_NOTE}"
        return gold["doi"], link, claim_block(twin["base_gold_id"])
    gold = json.loads((GOLD / "gold" / f"{target}.json").read_text())
    return gold["doi"], f"{gold['package']['url']} ({gold['package']['version_pin']})", claim_block(target)


def run(target, args):
    out_dir = HERE / "runs" / args.config
    out_dir.mkdir(parents=True, exist_ok=True)
    cert_out = out_dir / f"{target}-certificate.json"
    if cert_out.exists():
        return target, "already collected", 0
    doi, link, claims = target_info(target)
    prompt = (HERE / "prompt.txt").read_text().replace("{claims}", claims)
    if target.startswith("S-"):
        prompt = prompt.replace("This list\nis your approved claim list; you may add further claims "
                                "numbered from C100.", "The note below replaces the list.")
    prompt = prompt.replace("Article link or DOI:", f"Article link or DOI: https://doi.org/{doi}")
    prompt = prompt.replace("Code & Data link:", f"Code & Data link: {link}")
    rundir = WORK / "runs" / args.config / target
    if rundir.exists():
        shutil.rmtree(rundir)
    rundir.mkdir(parents=True)
    rlib = WORK / "rlib"
    rlib.mkdir(exist_ok=True)
    (rundir / "rlib").mkdir()
    env = {**os.environ, "R_LIBS_USER": f"{rundir / 'rlib'}:{rlib}",
           "XDG_CACHE_HOME": str(rundir / ".cache"),
           "UV_CACHE_DIR": str(WORK / "uv-cache")}
    cmd = ["codex", "exec", "-m", args.model, "-c", f'model_reasoning_effort="{args.effort}"',
           "-s", "workspace-write", "-c", "sandbox_workspace_write.network_access=true",
           "--add-dir", str(WORK / "uv-cache"),
           "--skip-git-repo-check", "-C", str(rundir), "--json",
           "-o", str(rundir / "last-message.txt"), "-"]
    (WORK / "uv-cache").mkdir(exist_ok=True)
    start = time.time()
    with open(rundir / "codex-events.jsonl", "w") as log:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, stdout=log,
                                  stderr=subprocess.STDOUT, env=env, timeout=args.timeout * 60)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            code = "timeout"
    minutes = round((time.time() - start) / 60, 1)
    certs = sorted(p for p in rundir.rglob("certificate.json") if ".cache" not in p.parts)
    if not certs:
        return target, f"no certificate (exit {code})", minutes
    shutil.copy(certs[0], cert_out)
    md = certs[0].with_name("certificate.md")
    if md.exists():
        shutil.copy(md, out_dir / f"{target}-certificate.md")
    return target, f"collected (exit {code})", minutes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=75, help="minutes per run")
    ap.add_argument("targets", nargs="+")
    args = ap.parse_args()
    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda t: run(t, args), args.targets))
    log = HERE / "runs" / f"log-{args.config}.csv"
    new = not log.exists()
    with open(log, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["target", "model", "effort", "outcome", "minutes", "finished"])
        for target, outcome, minutes in results:
            w.writerow([target, args.model, args.effort, outcome, minutes,
                        time.strftime("%Y-%m-%d %H:%M")])
            print(target, outcome, minutes)
    rows = sorted(p.name.split("-certificate")[0]
                  for p in (HERE / "runs" / args.config).glob("*-certificate.json"))
    with open(HERE / "runs" / f"runs-{args.config}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["config", "target", "certificate"])
        for t in rows:
            w.writerow([args.config, t,
                        f"model-gating/benchmark/runs/{args.config}/{t}-certificate.json"])


if __name__ == "__main__":
    main()
