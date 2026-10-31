"""Derive the benchmark prompt from the public prompt.

Benchmark runs use the public prompt word for word, except that the artefact list is replaced
by a slim one (certificate, executed code, logs, lockfile), and the model checks a given,
verdict-free claim list (gold-set/claims/), so every gold claim is scored.
Rerun after every change to prompt.txt; the check fails if the public prompt's structure changed.

Usage: python3 model-gating/scripts/make_benchmark_prompt.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
public = (ROOT / "prompt.txt").read_text()

start = public.index("Work in a new directory")
end = public.index("Report whether the computation")
slim = """Work in a new directory `<slug>-certification`. Benchmark mode: produce only these files:
- certificate.json (to the schema below) and certificate.md
- the code you executed, including any fixes or translations, under code/
- logs/ with the console output of every run that produced a reported value
- a lockfile or session record of the environment you ran (renv.lock, sessionInfo() output,
  pip freeze or pixi.lock)
Skip myst.yml, the Snakefile, nanopublications, CITATION.cff, SIGN-OFF.md and flora-entry.json.
Check every claim listed under "Claims to check" below, keeping its id, with one result per
printed number (a coefficient and its p value are two results with the same claim_id). This list
is your approved claim list; you may add further claims numbered from C100. Do not read
existing reproduction or replication reports of this paper. For certificate fields you cannot
fill honestly in benchmark mode (github_url, certification_id), use
https://forrtproject.github.io/reprocrowd/ and RC-0000-000.

"""
bench = public[:start] + slim + public[end:]
bench = bench.replace("Article link or DOI:", "Claims to check:\n{claims}\n\nArticle link or DOI:", 1)
bench = bench.replace("ReproCrowd reproduction check.", "ReproCrowd reproduction check (benchmark mode).", 1)
out = ROOT / "model-gating" / "benchmark" / "prompt.txt"
out.write_text(bench)
print(f"wrote {out.relative_to(ROOT)}")
