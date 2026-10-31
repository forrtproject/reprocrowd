# ReproCrowd reproduction certificate

**Outcome:** computational issues. The shipped Experiment 3 R script executed after one justified path adjustment. The prior-only heuristic AIC recurred at the reported precision; four other reported AICs did not recur. This is a computational assessment only. Scientific correctness and robustness were not checked.

**Paper:** [Learning From Aggregated Opinion](https://doi.org/10.1177/09567976241251741), Oktar, Lombrozo, and Griffiths (2024). **Code and data:** [OSF project](https://osf.io/dexuy/). The OSF data remain outside this bundle.

**Standard and engine:** crowd-repro v1.1.0; ReproCrowd benchmark prompt 0.1.2. Engine: Codex. Model and provider: GPT-6, OpenAI. Audit date: 2026-10-31.

**Environment:** macOS Tahoe 26.7 (arm64), R 4.6.1. Exact loaded package versions and platform details are recorded in [sessionInfo.txt](sessionInfo.txt).

## Results

| Claim | Reported AIC | Recomputed AIC | Status | Basis |
|---|---:|---:|---|---|
| C1 Proportion-opinion heuristic | 1722 | 1766.298 | discrepant | justified_fix |
| C2 Prior-only heuristic | 922 | 922.1692 | match | justified_fix |
| C3 Bayes-only predictor | 410 | 463.1 | discrepant | justified_fix |
| C4 UPCO-only predictor | 497 | 569.8 | discrepant | justified_fix |
| C5 Competence-only predictor | 507 | 785.1 | discrepant | justified_fix |

C1 and C2 are printed by the shipped script’s mixed-effects calls with random intercepts for Subject and lab. C3–C5 map to the corresponding single-predictor rows in its printed MuMIn model-selection table. The same table also contains ensembles: Bayes+UPCO has AIC 418.9, and UPCO+Competence has AIC 505.4. These are not single-model matches for C3–C5. The script does not contain separate mixed-effects calls for these three predictors comparable to the calls for C1 and C2.

## Execution and fixes

The executed copy of `E3_analysis.R` is in [code/E3_analysis.R](code/E3_analysis.R). Its only change was commenting out `setwd(r"(YOUR DIRECTORY HERE)")`, which is an unusable placeholder. I ran it with the OSF `e3_data.csv` as the working-directory input. No analysis code, model specification, sample, or data were changed. The run installed missing packages `gmp`, `qualtRics`, and `MuMIn` (plus their dependencies); versions are in `sessionInfo.txt`.

The full console output is [logs/E3_analysis_run1.log](logs/E3_analysis_run1.log). The source script checksum matches the supplied OSF SHA-256. The downloaded data SHA-256 is recorded in `certificate.json`; the data file itself is not included.

## FORRT chain outcome

`outcome_computational`: **computational issues**. `outcome_robustness`: **not checked**. The computation was executable with a path-only justified fix; only C2 reproduced among the approved claims. See [certificate.json](certificate.json) for claim-level results, provenance, and findings.
