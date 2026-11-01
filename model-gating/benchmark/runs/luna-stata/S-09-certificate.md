# ReproCrowd reproduction check

**Paper:** Gsottbauer et al. (2022), *Social class and (un)ethical behaviour: causal and correlational evidence*, DOI [10.1093/ej/ueac022](https://doi.org/10.1093/ej/ueac022).  
**Outcome:** **computational issues**. This checks computational reproducibility and makes no judgement about the scientific conclusion.  
**Procedure:** ReproCrowd crowd-repro v1.1.0 · **Engine:** Codex · **Model/provider:** GPT-6 / OpenAI · **Date:** 2026-11-01.  
**Environment:** R 4.6.1 on macOS Tahoe 26.7 (aarch64); see `sessionInfo.txt`.

## What recurred

The translated pipeline ran to completion on the package’s supplied data. Survey 1 manipulation-check cell means (4.83, 5.69, 5.54, 6.54) and payment cell means (11.20, 11.16, 11.19, 10.28) recur at their printed precision. Survey 1 payment regression coefficients and sample sizes also recur at the reported precision. Survey 2 cell means and core payment regression terms recur. Table 9 subgroup Ns (807 overall, 651 for the extent question) and descriptive means are consistent with the paper.

The belief survey has 808 rows; one lacks income classification, leaving 807 for the real-rich subgroup comparisons. Survey 1’s upstream GIP wave merge cannot be reconstructed because its wave inputs are not included. The authors’ main script comments out that step and reads the supplied anonymized master file.

## Limits

Stata was unavailable, so the shipped Stata scripts were translated into R. The translation covers available data cleaning, summaries, rank-sum tests, robust regressions, and payment frequency summaries. Stata `ksmirnov` and `bitest` diagnostics and exact figure exports were not reproduced. Those values are marked `not_checkable`; student-specific means printed in prose are not produced by the shipped result commands. The certificate lists focal table results and records that it is not an exhaustive inventory of every numeric mention in the article.

No package code or data was copied into this bundle. The package used was `/tmp/scratch_bench_luna/packages/pkg-c4501c`.

## FORRT chain vocabulary

This is a **Reproduction Study** using the same methodology, translated directly to R because Stata was unavailable. `outcome_computational` is **computational issues**; `outcome_robustness` is **not checked**. See `certificate.json`, `logs/full_run.txt`, and `code/`.
