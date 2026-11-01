# ReproCrowd reproduction check

**Engine:** Codex · GPT-6 · OpenAI · **Rules:** crowd-repro v1.1.0  
**Procedure:** Reproduction Study (same methodology; direct Stata-to-R translation for the primary reported models)  
**Date:** 2026-11-01  
**Paper:** Kristian Vrede Skaaning Frederiksen (2022), “Does Competence Make Citizens Tolerate Undemocratic Behavior?” [DOI](https://doi.org/10.1017/S0003055422000119)  
**Code and data:** local package `/tmp/scratch_bench_luna/packages/pkg-984353` (not uploaded). Article copy: `/tmp/scratch_bench_luna/articles/pkg-984353/article.pdf`.

## Outcome

**FLoRA outcome_computational: computational issues.** The translated primary regressions execute on the supplied final dataset. Reported country endpoints for the effect of undemocratic behavior and the Czech interaction estimate, interval, and p value recur at printed precision. The sample counts do not recur: the supplied dataset has 16,777 unique respondents and 335,540 candidate rows, compared with 14,058 respondents and 267,795 candidates in Figure 1. The country-specific data counts also exceed the printed ranges. This is a computational discrepancy, not a judgment about the paper’s scientific conclusion.

**FLoRA outcome_robustness: not checked.** No robustness or scientific-validity assessment was performed.

## What was run

`code/translated_analysis.R` translates the shipped Figure 1 interaction regressions and Table A1 additive regressions. It imports only the required columns from `dataset.dta`, preserves the five-level competence factor and category 3 reference, and calculates respondent-clustered HC1 standard errors. `logs/translated_analysis.log` contains the run output. Model estimates include South Korea −0.0647 and the United States −0.2007 for undemocratic behavior at average competence. The Czech difference between very incompetent and average-competence candidates is 0.1285; its translated 95% confidence interval is approximately [0.0508, 0.2062] and p = 0.00120. These round to the corresponding reported values.

The data preparation stage is not rerunnable from the supplied package. `Data_prep.do` begins by importing country survey exports such as `ukmain.tsv`; no such TSV inputs are present. It also references a hard-coded Windows `U:` drive. Stata is not installed. The package does include `dataset.dta`, which enabled the direct translation of the primary analysis models. A command-by-command R translation of the entire 2,755-line preparation script was not completed; results depending on its unavailable raw inputs were not checked. The package dataset’s count mismatch remains unexplained and could reflect a different release or an undocumented sample restriction; no sample was changed to force a match.

## Claims checked

The certificate assigns C1–C10 to the article’s data-derived numeric claims. Each reported endpoint, estimate, p value, interval endpoint, or count has an individual result in `certificate.json`. The abstract contains no data-derived numeric result. Numeric design details and profile scale labels were not treated as results. Tables 1 and 2 describe treatment levels rather than computed results.

## Environment

Host: macOS Tahoe 26.7 (details in `logs/host-os.txt`). R 4.6.1; `readstata13` 0.11.0; `sandwich` 3.1-3; dependencies recorded in sessionInfo include `zoo` 1.9-1, `Rcpp` 1.1.2, and `lattice` 0.22-9. Full `sessionInfo()` is in `logs/sessionInfo.txt`. Stata is not installed. The original `.do` scripts and `Power.R` remain only at the supplied package path; they were not copied into this bundle. The executed analysis translation is `code/translated_analysis.R`.

## FORRT chain record

This is a **Reproduction Study**. The computation was checked and yielded both recurring and non-recurring results. The certificate records the computational outcome as **computational issues** and the robustness outcome as **not checked**. Source data and code remain at the local package path above; none were uploaded.
