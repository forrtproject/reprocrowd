# Reproduction check: “Safe Assets”

**FORRT computational outcome:** computational issues  
**ReproCrowd standard:** crowd-repro v1.1.0  
**Procedure:** ReproCrowd benchmark prompt v0.1.2  
**Engine:** Codex · rules: crowd-repro v1.1.0  
**Model/provider:** GPT-6.1 Luna / OpenAI  
**Audit date:** 2026-11-01  
**Environment:** macOS Tahoe 26.7, arm64; R 4.6.1. Package versions are in [sessionInfo.txt](sessionInfo.txt).

## Outcome

The translated empirical pipeline reproduces the reported Table 1 country values and most summaries, Table 2 sector-composition values, Table 3 regression coefficients and standard errors, and all Table 4 portfolio shares at their printed precision. One Table 1 summary is discrepant: the paper's minimum central-bank share is 0.01, while the translated shipped preparation produces 0.00 because it replaces missing central-bank components with zero. The discrepancy is retained as reported. The empirical code uses the supplied data and preserves the paper's definitions and samples. The result basis is `translated`; the direct translation and console output are in [reproduce_empirical.R](code/reproduce_empirical.R) and [empirical_run.log](logs/empirical_run.log).

The paper's model simulations in Tables 5–7 and Figure 3 were not run. The shipped MATLAB code and model inputs are present, but MATLAB, its required toolboxes, and Octave are unavailable in this environment. Those printed model results are therefore listed as `not_checkable` and `not_computed`; they are not presented as reproduced. The return columns in Table 2 are also not checkable from the shipped pipeline because their source series are not included.

In the FORRT reproduction chain, the input was the supplied [article](https://doi.org/10.1093/ej/ueac017) and local package at `/tmp/scratch_bench_luna/packages/pkg-93cd12` (also linked by the authors at [Zenodo](https://zenodo.org/records/5979683)). The computation step translated and ran the Stata empirical scripts in R. The results step compared the printed tables with the translation output. The reproduction outcome is computational issues because the separate simulation pipeline remains unchecked. The assessment concerns computation only and does not assess the scientific conclusion.

## Translation and changes

The R script translates the complete Stata empirical pipeline: OECD and GDP preparation, currency-specific reshapes and joins, variable construction, Tables 1–3 summaries and regressions, Table 4 weighted SCF calculations, and the Figure 1 and Figure 2 line-chart commands. It reads the original CSVs and SCF Stata file from the supplied package; none of the original data or code were copied into this certificate bundle.

Changes were limited to language/runtime translation and paths: Windows backslash paths and Stata `insheet`, `reshape`, `joinby`, `summarize`, `reg`, and `xtreg, fe` operations were expressed with R imports, reshapes, joins, weighted summaries, OLS, and country fixed effects. SCF percentiles use the inverse weighted empirical CDF; the printed Table 4 values match the Stata article table at one decimal place. No data, sample, exclusion, or model specification was changed. Temporary plot files were removed after the translated graph commands ran.

The script's merge retains additional rows with no numeric Table 1/2 outcome; the comparison output filters those all-missing rows for readability. The 34 complete OECD rows and the calculations for reported summaries are unchanged. A warning about New Zealand's absent USD series is logged; it does not affect the reported table values.

## Claim coverage

The certificate contains one result for each numeric cell in Tables 1, 2 (sector composition), 3, and 4, the reported external return cells in Table 2, and the numeric entries in Tables 5–7. It also records selected text-reported baseline and Figure 3 values. Table 1 and Table 2 external real-return columns that rely on external data, and model-generated Table 5–7/Figure 3 values, have explicit reasons and statuses in `certificate.json`.

## Reproduction chain files

- `certificate.json`: machine-readable ReproCrowd certificate and result records.
- `code/`: executed R translation and certificate builder.
- `logs/`: console output from the empirical run.
- `sessionInfo.txt`: R and package environment record.

Original data/code were not uploaded. No nanopublication, Snakefile, or other non-benchmark files were created.
