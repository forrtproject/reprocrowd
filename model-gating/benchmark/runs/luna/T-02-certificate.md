# Reproduction Study: Entertaining Beliefs in Economic Mobility

**Outcome:** computational issues. The shipped R script ran successfully and reproduced four of the five approved coefficients at the printed three-decimal precision. It yielded 0.057 for C1, while the approved claim is 0.055. This report assesses computation only; it does not assess whether the scientific conclusion is correct.

**Paper:** Eunji Kim (2021), “Entertaining Beliefs in Economic Mobility,” [doi:10.1111/ajps.12702](https://doi.org/10.1111/ajps.12702). **Code and data:** the local shipped package at `/tmp/scratch_bench_luna/packages/T-02` (not uploaded).

## Results

| Claim | Reported | Recomputed by shipped code | Status |
|---|---:|---:|---|
| C1 MTurk treatment, Table 1 column 1 | 0.055 | 0.057 | Discrepant |
| C2 Lab-in-the-field treatment, Table 1 column 5 | 0.068 | 0.068 | Match |
| C3 Frequent viewer, Table 2 column 2 | 0.032 | 0.032 | Match |
| C4 Heavy viewer, Table 2 column 2 | 0.040 | 0.040 | Match |
| C5 Occasional viewer, Table 2 column 2 | 0.013 | 0.013 | Match |

The C1 gap is 0.002, greater than one unit at the last printed decimal. Because this is a deterministic OLS result and no identifiable reporting slip explains the difference, it is classified as discrepant rather than close. The script’s C2 and Table 2 values recur exactly at the precision printed in the manuscript. The approved claim list asked for coefficients only, so no p-value claims are assessed.

## Execution and environment

The original `AJPS_2021_Kim_Manuscript.R` was executed unchanged from the package directory. No data or model specification was changed. The script uses relative `load()` paths, so the working directory must contain the shipped data. The successful execution exited with status 0. Its output is recorded in `logs/manuscript-run-4.txt`; the executed script copy is in `code/`.

Engine: Codex · model: GPT-6 · provider: OpenAI · rules: ReproCrowd crowd-repro v1.1.0 · procedure: 0.1.2. Environment: R 4.6.1 on macOS Tahoe 26.7, aarch64-apple-darwin23. `sessionInfo.txt` records loaded packages; `R-packages.txt` records the complete installed R package inventory.

The run produced a many-to-many join warning in the NYT text analysis and a warning that `geom_col()` ignored `size`; both occurred before the target table output, and the script completed successfully.

## FORRT nanopublication chain vocabulary

This artefact records the chain stages as **reproduction study** → **computational reproducibility check** → **outcome: computational issues** → **robustness: not checked**. This benchmark bundle omits the nanopublication files as instructed.

## Finding

**REPRO-001 (P1):** the shipped script’s MTurk treatment estimate differs from the approved printed value. The paper’s 0.055 should be checked against the archived output; this reproduction leaves the code and data untouched.
