# Seeded twins v1.0

Eight twins, each based on a different gold v1.0 paper, with one planted change to an author-written analysis file. All original numerical sections reproduce the gold matching claims; G-08 C4 confirms the already documented `close` result. The twins are outside the 30-paper gold set and must be scored separately. All eight have expected paper status `computational issues`.

| Twin | Base paper | Single perturbation | Affected claims | Severity | Original / twin seconds |
|---|---|---|---|---|---:|
| [T-01](T-01/twin.json) | G-01 · Loneliness trajectories | Multiply study SEs by 1.001 | C3, C4 | P2 | 2.246 / 2.278 |
| [T-02](T-02/twin.json) | G-02 · Entertaining beliefs | Omit optimism covariate in MTurk model | C1 | P1 | 0.146 / 0.164 |
| [T-03](T-03/twin.json) | G-04 · Risky-choice framing | Reverse binary Choice in CloudResearch sample | C1, C3, C5 | P2, P1, P1 | 0.977 / 0.911 |
| [T-04](T-04/twin.json) | G-06 · Black workers in white places | Use House-vote outcome in presidential model | C1 | P1 | 1.814 / 1.749 |
| [T-05](T-05/twin.json) | G-08 · Transitional justice museums | Replace mean imputation with zero imputation | C1–C5 | P1 | 0.328 / 0.328 |
| [T-06](T-06/twin.json) | G-12 · Gambler’s fallacy | Invert Experiment 1a base-rate subset | C1 | P1 | 0.281 / 0.371 |
| [T-07](T-07/twin.json) | G-19 · Proenvironmental behavior and well-being | Omit final activism indicator from PEB count | C1, C2 | P2 | 2.048 / 1.399 |
| [T-08](T-08/twin.json) | G-30 · Incentives across cultures | Disable UK duplicate-submission exclusion | C3, C4, C5, C7, C8 | P1, P1, P1, P2, P2 | 1.112 / 1.029 |

There are 20 affected claims: 13 P1 and 7 P2. Affected claims have `expected_status: discrepant` and only `discrepant` in `acceptable_statuses`. Unaffected claims retain their gold status and alternatives, with the actual twin-run value as the scoring reference. Raw numerical movement below printed precision does not make an otherwise matching claim discrepant.

The set includes small changes as well as sign reversals and a wrong subset. For example, T-01 moves I-squared from **98.74 to 98.73**; T-07 moves the PEB mean from **2.11 to 2.10** and SD from **0.98 to 0.97**. T-02 moves a treatment coefficient from **0.055 to 0.057**. These values come from the retained execution logs.

P1/P2 follows reconciliation rule R2. Heterogeneity summaries and activity descriptives are P2. In T-03 the standard-frame comparison C1 is secondary to the script’s explicitly named `PRIMARY MODEL`; the primary-model VDA and Frame coefficients C3/C5 are P1. In T-08 the specific flat-fee contrast and cost-effectiveness comparison are secondary (P2).

## Files and execution scope

Each twin directory contains:

- `twin.patch`: one unified-diff hunk against the pinned original analysis file, containing only the planted change. The header includes a tab separator so paths containing spaces work with macOS `patch`.
- `twin.json`: source package pin, perturbation, R4 setup/path repairs, exact numerical execution scope, R/package versions, measured runtimes, every base claim’s original and twin values, statuses, severity and hard-coding signal.
- `run_original.log` and `run_twin.log`: trimmed actual output, including every claim value, run-result JSON, session information and relevant warnings.
- `input_manifest.json`: third-party input locations, versions and content hashes. The required China input for T-08 has an additional explicit pin described below.

[`reproduce.R`](reproduce.R) is the small selection/extraction harness. It evaluates the authors’ numerical expressions in their original order and prints all gold claim values. It applies documented input-path resolution in memory. It does not contain replacement statistical models or target values. For T-08 C8 it evaluates the author-written Welch test expression for the UK Monetary/Norm comparison; the comparison selector is fixed to that claim.

The execution scope covers **every selected gold claim**, not every analysis in each package. Unrelated figures, table rendering, corpus analyses, Bayesian models and other studies are not claimed as executed. Each `execution_scope` identifies the precise sections and objects. In particular, G-01 starts from the public deposited study-level summaries, as its gold record specifies; the individual-level studies are outside scope. No intermediate input was replaced by a newly calculated or repaired dataset.

R is **4.6.1 (2026-06-24)**. Times in the table are elapsed seconds measured inside R for the stated numerical scope, including its library loads and excluding package downloads/installation. Missing dependencies were installed into `/tmp/scratch_gold2/sol/rlib`; existing user/system libraries remain available. Mixed-model singular-fit warnings for G-19 occur in both the original and twin and are retained.

Third-party packages and data remain in `/tmp/scratch_gold2/sol/`, outside the repository. About **2.69 GB** of completed third-party original-file payloads were saved during selection, including unused candidates and an initially broader G-01 download; temporary dependencies and copies are additional disk use, not further package downloads. Unused large downloads were removed after verification. Neither gold, labels nor claims were edited, and nothing was committed.

## Verification and rerunning

[`verification.json`](verification.json) records the independent clean-copy check for each twin. For each run, the checker rebuilt a package from hash-verified original inputs, applied `twin.patch` for the twin copy, then executed the retained `reproduce.R`. Both processes must exit zero, all claim values must agree with the recorded run at printed precision, and the computed affected-claim set must equal the labels. Every patch must contain one hunk and apply without rejects.

The temporary copies used for that check have been deleted. To rebuild a twin package from the hash-pinned inputs, run `python3 model-gating/benchmark/build_twin_package.py T-07 /tmp/scratch_twins/T-07` from the repository root (it downloads the manifest inputs, checks every SHA-256 and applies `twin.patch`). The original check ran commands of this form, which need the original copy and an R library with the packages installed:

```sh
R_LIBS=/tmp/scratch_gold2/sol/rlib TMPDIR=/tmp/scratch_gold2/sol/tmp Rscript --vanilla model-gating/gold-set/twins/reproduce.R G-19 /tmp/scratch_gold2/sol/verify/T-07/original
R_LIBS=/tmp/scratch_gold2/sol/rlib TMPDIR=/tmp/scratch_gold2/sol/tmp Rscript --vanilla model-gating/gold-set/twins/reproduce.R G-19 /tmp/scratch_gold2/sol/verify/T-07/twin
```

For a new download, retrieve the manifest inputs at the recorded versions and verify their SHA-256 hashes before applying the patch. G-01’s Git LFS inputs require the manifest’s media URLs or `git lfs pull` at the pinned commit; the raw GitHub URL can return a pointer. Preserve deposited paths. Apply a twin patch to its own copy before running the harness; do not include `twin.json`, logs, this README or scoring references in the package given to a benchmark model. Give that model the original paper and the patched analysis package.

## Findings about gold v1.0

**No new numerical contradiction was found in the eight bases.** Every `match` claim rounds to its printed value in the original run. G-08 C4 recomputes to **0.1980144569**, confirming the existing gold `close` label and reference 0.198; it rounds to 0.20 rather than the printed 0.19. Its `original_run.claims[].recurs` is therefore `false`, deliberately distinguishing literal printed recurrence from confirmation of an existing close label. This is not a newly discovered gold error.

**G-30 has an incomplete input pin.** Its gold record pins the Study 2 script and UK data but omits the required `Study2A_RAW_China_deidentified.xlsx`. The twin manifest adds original OSF file **64b3b2104eade909adfa7b5e, version 1**, SHA-256 **aa31cfe5ef9ce27725b595cd257e27cee236ae657f8aa485c47cb50efd192bcb**. That deposited input reproduces all six gold claims. The gold record remains unchanged; this is a provenance finding, not an execution discrepancy.

G-04’s previously low-confidence blanket-source labels now have numerical confirmation for all six selected claims. Its C1/C2 map to `StdFE`, the standard G4/L6 comparison, not the all-cell `mlr0` model.

## Discarded trials and limitations

A median-imputation trial for G-08 changed raw coefficients but none at printed precision, so it was discarded. An exploratory single-response edit in G-04’s deposited clean CSV was replaced with the script-level reverse-code seed: rerunning the authors’ cleaner should not erase a twin. A first patch-application check rejected paths containing spaces; the final tab-delimited headers passed the clean-copy check.

Several initial attempts needed local dependency loading or a correction to the selection harness’s line ranges/model mapping; none is treated as a base-paper failure. G-05, G-11 and G-13 were downloaded as fallbacks but were not executed or used for twins. The final eight have no unresolved execution failure. The selective numerical scope and additional G-30 input pin remain explicit limits of the verification.

## Second check (Claude, 30 October 2026)

Claude inspected the eight patches (one changed or added line each; `reproduce.R` contains no
hard-coded target values) and reran all 16 runs from fresh copies of the hash-verified originals,
applying each `twin.patch` independently. All runs exited cleanly, every recomputed claim value
agreed with the values recorded in `twin.json`, and the affected-claim sets match. T-01 (SEs
multiplied by 1.001) and T-03 (an added reverse-coding line) are visibly artificial if a reader
inspects the code closely; the other six resemble ordinary analyst slips.
