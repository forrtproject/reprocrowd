# Benchmark runs: approach and first results

The benchmark design is in [`SPEC.md`](SPEC.md) (draft 0.4, agreed with Sol and Argon on
1 November 2026). This README describes the **pilot**, which the specification supersedes. The
pilot ran on gold v1.3 with the gold claim list always supplied, remote packages for gold papers, a
shared R library and no isolation. `run_codex.py` is the pilot runner; section 7 of the
specification defines its replacement. The pilot results are diagnostic only.

This folder runs model configurations on the gold set (`../gold-set/`) and scores them. The first
configuration is GPT-6 Luna through the Codex CLI on the ChatGPT subscription, at the default
reasoning effort (medium). So far it has run on five targets: G-08, G-21 and G-23 plus twins T-02
and T-06. The full run (30 papers and 8 twins) waits for Lukas to approve the approach below.

## How a run works

1. `run_codex.py` creates a fresh directory per target under `/tmp/scratch_bench_luna/runs/`,
   outside the repository, so the gold files, labels and twin metadata are out of reach. The
   agent is told to work only there and not to read existing reproduction reports. This relies on
   the agent following the instruction; network access is open because packages must be
   downloaded.
2. The prompt is `prompt.txt`, generated from the public `prompt.txt` by
   `../scripts/make_benchmark_prompt.py`. It is the public prompt (v0.1.2, rule pack v1.1.0) with
   two changes:
   - it asks for a slim bundle: certificate, executed code, logs and an environment record;
   - it lists the gold claims to check, verdict-free (claim, location, printed value), from
     `../gold-set/claims/`. The model may add its own claims from C100.
3. Twins get a local package rebuilt by `build_twin_package.py`, which downloads the
   hash-pinned inputs and applies the planted change. Nothing in the package or prompt says it is
   a twin. The paper DOI is the real one.
4. The certificate is copied to `runs/<config>/` and scored with
   `../scripts/score_certificate.py runs/runs-<config>.csv`.

Run more targets with:

```sh
python3 model-gating/benchmark/run_codex.py --config luna --model gpt-6-luna --effort medium --jobs 5 G-01 G-02 T-01
```

## Why the claim list is given

The first batch (`runs/luna-batch1-ownclaims/`) let the model choose its own claims, as the
public workflow does. It addressed only 11 of 27 gold claims; on T-06 it never listed the
planted claim. Scores then mostly measured claim selection. With the claim list (batch 2), every
gold claim was addressed. Claim selection still matters for public use, but it needs its own test,
for example by comparing a model's own list with the gold list.

## Scores, batch 2 (gold v1.3, five targets)

| Metric | Luna |
|---|---|
| Schema-valid certificates | 5/5 |
| Paper status correct | 5/5 |
| Claim outcome correct (reproduces vs does not) | 22/26 |
| Claim status correct | 21/26 |
| Specificity (gold match/close not flagged discrepant) | 16/19 |
| Sensitivity, P1+P2 | 3/4 (P1: 2/2, both planted twin errors) |
| Blocked claims reported as not reproducing | 3/3 |
| Hard-gate violations | 0 |
| Minutes per run | 2.4 to 6.4 |

Five targets cannot rank a model. The five wrong claims come from two cases:

- **G-21 C3 to C5 (gold `match`, Luna `discrepant`).** The printed AICs come from a mixed-effects
  variant that the authors' script describes in a comment but does not run. Run as shipped, the
  script gives 463, 570 and 785 against the printed 410, 497 and 507. Gold accepts the documented
  option; rule pack 1.1.0 does not mention such options, so Luna's reading is defensible. This
  needs a decision (see the report).
- **G-23 C3 and C4 (gold `match` and `discrepant`, Luna `not_checkable`).** The script crashes
  earlier on a missing object. The two statistics do not depend on it, but reaching them means
  running the statements after the crash. Luna stopped at the crash. For C4 the outcome (does not
  reproduce) is still right.

## Files

- `run_codex.py`, `build_twin_package.py`, `prompt.txt`
- `runs/luna-batch2/`: batch 2 certificates; `runs/runs-luna-batch2.csv`,
  `runs/log-luna-batch2.csv`, `runs/scores-luna-batch2.json`. The T-02 and T-06 packages in this
  batch still contained rendered outputs; twin packages now omit them
  (`../gold-set/twins/strip_outputs.json`), so these two certificates are a record only.
- `runs/luna-batch1-ownclaims/`: batch 1 (no claim list), kept for comparison
