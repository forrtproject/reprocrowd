# ReproCrowd reproduction certificate

**Paper:** Holt, “Examining inequality in the time cost of waiting” (2023), [doi:10.1038/s41562-023-01524-w](https://doi.org/10.1038/s41562-023-01524-w)  
**Outcome:** technical failure  
**ReproCrowd rules:** crowd-repro v1.1.0  
**Procedure:** ReproCrowd benchmark prompt 0.1.2  
**Engine:** Codex · GPT-6 · OpenAI  
**Date:** 2026-11-01

## Result

The computation was not executable end to end from the supplied package. Stata was not installed, so the master pipeline was attempted through an R translation entrypoint. The first cleaning stage requires five raw ATUS files that are not in the package. Only a preprocessed `atusall0319.dta` intermediate is supplied. The run stopped before producing a reported value. The paper's headline estimates and selected descriptive values are therefore `not_checkable`; no scientific conclusion is assessed.

The imputation stage independently refers to a federal poverty-threshold dataset at `draft/nature/check/federal_poverty_threshold.dta`, also absent from the package. The supplied CPS ASEC dataset does not replace this input.

## Findings

- **DATA-001 (P0):** Raw ATUS roster, CPS, response, summary and activity inputs are missing. `logs/pipeline-run.log` records the failed input check.
- **DATA-002 (P0):** Federal poverty-threshold data needed by `05_imputation.do` are missing.
- **CODE-001 (P0):** Stata was unavailable. The R translation entrypoint checked the specified master order and stopped at the missing raw inputs. No estimates were recomputed.

## Values checked

`certificate.json` preserves the paper's reported headline probabilities, conditional waiting times, annualized gaps, sample sizes, and selected descriptive means. Their computed values are unavailable because the pipeline could not run, so each is listed as `not_checkable` with `basis: not_computed`.

## Limitations

This benchmark certificate does not provide a complete cell-by-cell inventory of all numerical content in the article PDF. It captures selected headline and descriptive values only. The translation artifact is a master-pipeline input and dependency check, not a complete command-by-command translation of all cleaning, table, figure, and imputation commands. Those omissions prevent this bundle from satisfying the requested exhaustive claim enumeration and full translation; the reported technical failure and missing-input evidence remain valid for the attempted run.

No original data or code were uploaded. The package files were copied into `code/source/` only as shipped source for this local certification bundle; no data files were copied.

## Reproduction chain

This is a FORRT-chain reproduction study with outcome `technical failure` and `outcome_robustness = not checked`. It reports computational executability only and does not judge the scientific conclusion.

## Environment

R 4.6.1 on the Linux container. Stata was not installed. The session record and installed R package inventory are included as `sessionInfo.txt` and `session-packages.csv`.
