# ReproCrowd certification

**Outcome:** computational issues. The analysis scripts were translated directly from Stata to R because Stata is unavailable. Tables 3, 4, 6, 7 and 9 summary values and sample counts checked here recur at their printed precision. Regression and rank test claims, and per-bin distribution-test p-values, are not comprehensively reconciled to every printed cell; the certificate records the scope and limitations. This report concerns computation only and does not assess the scientific conclusion.

**Paper:** Gsottbauer, Müller, Müller, Trautmann & Zudenkova (2022), *Social Class and (Un)Ethical Behaviour: Causal and Correlational Evidence*, DOI [10.1093/ej/ueac022](https://doi.org/10.1093/ej/ueac022).

**Code and data:** [local package directory](/tmp/scratch_bench_luna/packages/pkg-c4501c). The package’s shipped CSV and Stata files are used in place; none are copied into this bundle. The Survey 1 cleaning script references GIP source waves that are absent from the package, so the shipped anonymized master dataset was analyzed. Survey 2 and belief data are likewise taken from their shipped files.

**Procedure:** ReproCrowd crowd-repro v1.1.0. **Engine:** Codex · rules: 1.1.0. **Model/provider:** GPT-6 / OpenAI. **Date:** 2026-11-01. **Environment:** macOS aarch64; R 4.6.1; haven 2.5.5, sandwich 3.1-1, lmtest 0.9-40. See [sessionInfo](logs/sessionInfo.txt) and [run output](logs/translated_analysis.log).

## Translation and run

[translated_analysis.R](code/translated_analysis.R) translates the analysis-ready portions of the shipped Survey 1, Survey 2, and belief-survey Stata scripts: descriptive statistics, rank-sum tests, OLS specifications, and heteroskedasticity-robust standard errors. Paths were parameterized to the provided package. Stata labelled treatment values were converted to labels for correct group comparisons. Unclassified postal leading digits were represented by all-zero state indicators, matching Stata's false equality comparisons and retaining the full sample in the controlled Survey 2 model. The translation uses R's `wilcox.test` and sandwich HC1 covariance; those are close counterparts, not a Stata execution.

Summary means and Ns in the main manipulation-check and payment tables match at the precision printed. The belief-survey means, SDs and Ns also match at printed precision. Regression tables include coefficient and standard-error values, but every printed cell has not been reconciled in the claim ledger; some quantities have only a summary status in the run log. The rule pack requires a result per printed number, so this bundle’s result ledger is incomplete for the many Table 1/2 descriptives and Table 5/8 model cells. The overall status is therefore **computational issues**, and this limitation should be resolved before treating the certificate as exhaustive.

## FORRT nanopublication chain

This benchmark certificate does not emit a nanopublication or a new replication result. Its computational vocabulary maps to `outcome_computational: computational issues`; `outcome_robustness: not checked`. Benchmark placeholders are used for `github_url` and `certification_id` as instructed.
