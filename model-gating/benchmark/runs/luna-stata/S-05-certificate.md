# Reproducibility certificate: *Safe Assets*

**Outcome:** technical failure. **ReproCrowd rules:** v1.1.0. **Procedure:** 0.1.2. **Engine:** Codex · GPT-6 · OpenAI. **Date:** 2026-11-01. **Host:** macOS Tahoe 26.7, Apple Silicon.

## What was checked

The supplied package contains the Stata empirical pipeline (`Replicate_Empirical_Results.do`, including OECD data preparation and the SCF tables) and the MATLAB simulation pipeline (`Replicate_Simulation_Results.m`, including the model routines). The environment check found R 4.6.1 but no Stata, MATLAB, or Octave. The only executed R file, `code/runtime_check.R`, checks interpreter availability; it does not compute any paper results. Its console record is in `logs/runtime_check.txt`; the R session record is `sessionInfo.txt`.

No article number is marked as reproduced or discrepant. The records in `certificate.json` are `not_checkable` because no recomputation was performed. In particular, this bundle does not satisfy the requested command-by-command translations, full pipeline coverage, or one-result-per-printed-number inventory. C14 and C15 explicitly flag grouped and omitted coverage. Treat this as a transparent partial failure record, not as a completed Reproduction Study.

## Findings

- **RUN-001 (P0):** Required statistical runtimes are absent. There are no computed comparisons, so reproducibility of the reported values is undetermined.
- **COV-001 (P1):** The article's full set of data-derived numbers was not individually enumerated. Tables 6–7 and figure coordinates are grouped or omitted, as are many table cells and repeated numerical claims in the text.

The package files and data were not copied into this bundle. Package location: `/tmp/scratch_bench_luna/packages/pkg-93cd12`. Article PDF: `/tmp/scratch_bench_luna/articles/pkg-93cd12/article.pdf`. The article points to the original replication package at [Zenodo record 5979683](https://zenodo.org/records/5979683). No existing reproduction report was consulted.

**FORRT chain vocabulary:** outcome_computational = `technical failure`; outcome_robustness = `not checked`. No conclusion is made about scientific correctness.
