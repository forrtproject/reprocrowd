# ReproCrowd reproduction certificate

**Outcome: technical failure.** The shipped R analysis ran through the Group 1 calculations and reproduced selected STAT and task-comparison results. It then stopped because `GMHWG` is undefined. The script itself says the Group 2 analysis is omitted, so the workflow does not produce later group comparisons or the reported Table 9 correlations. The computation is therefore not fully executable or reproducible as shipped, despite the partial matches.

## Procedure and environment

- **Engine:** Codex
- **Model and provider:** GPT-6 · OpenAI
- **Rules:** ReproCrowd `crowd-repro` v1.1.0
- **Procedure:** ReproCrowd benchmark prompt 0.1.2
- **Date:** 2026-10-31
- **Host:** macOS Tahoe 26.7, Apple Silicon
- **R:** 4.6.1; package versions and loaded dependencies are recorded in [sessionInfo.txt](sessionInfo.txt). Python extraction details are in [python-environment.txt](python-environment.txt).
- **Python:** 3.14.6; `py7zr` 1.1.4 was used only to extract the supplied archive.

The only adjustments were execution setup: install the packages missing from the environment, point the working directory at the extracted data, and suppress interactive `View()` calls at runtime. These do not change the analysis. The original script is preserved in `code/survey_2021.R`; `code/run_analysis.R` is the capture wrapper. The wrapper catches the script's fatal error only so already computed objects and the error can be logged. It does not add analysis. No data or code was uploaded.

## Claim → Evidence → Method → Result → Interpretation → Conclusion

**Claim.** The selected paper results are reproducible and the full workflow can regenerate its reported outputs.

**Evidence.** The version 1 Figshare script and dataset hashes match the supplied SHA-256 values. In the run log, the sample STAT score is 10.62 (SD 2.45), matching Section 4.3. Group 1 Task 1 counts are 13/37 versus 32/37, and the McNemar statistic is 15.43 (p < .001), matching Table 1. The Group 1 overall GM-BM Wilcoxon V = 78 and p = .012 recur, while the computed lower confidence bound is -1.0 rather than the paper's -1.5. The console then reports `object 'GMHWG' not found`.

**Method.** Executed the supplied R script against Figshare article 22132940 version 1 data in R 4.6.1. Only package installation, working-directory setup, and suppression of interactive viewers were used as justified execution fixes. No missing code was written.

**Result.** Two selected results match at printed precision; the Wilcoxon interval is discrepant; Table 9's STAT/Google Maps correlation and the remaining downstream group comparisons are not checkable because the script fails first. The CSV for Group 2 exists, but the shipped script explicitly omits the code that would build `GMHWG` from it.

**Interpretation.** This is a computational limitation in the supplied workflow, not an assessment of the scientific conclusion. The confidence-interval discrepancy may reflect R version drift, but that cause is not established.

**Conclusion.** Under FORRT's `outcome_computational` vocabulary, this reproduction is **technical failure**: the full shipped computation cannot complete. `outcome_robustness` is **not checked**.

## Claim results

| Claim | Reported | Recomputed | Status |
|---|---|---|---|
| C1. STAT score mean ± SD | 10.62 ± 2.45 | 10.62 ± 2.45 | Match |
| C2. Table 1, Task 1 success rates and McNemar test | 35.14% vs 86.49%; χ² = 15.43, p < .001 | 13/37 vs 32/37; χ² = 15.43, p < .001 | Match |
| C3. Table 4, GM-BM Wilcoxon test | V = 78, p = .012 | V = 78, p = .012 | Match |
| C4. Table 4, GM-BM 95% CI | [-1.5, 0.0] | [-1.0, 0.0] | Discrepant |
| C5. Table 9, STAT / Google Maps task score | τ = .29, z = 3.19, p = .001 | Not computed | Not checkable |
| C6. Group 2 and downstream Bing / HERE WeGo analyses | Tables 2, 3, 5, 7-9 | Not computed; script stops at `GMHWG` | Not checkable |

Every computed result has basis `justified_fix`; unavailable downstream results have basis `not_computed`. The exact fixes and claim details are in [certificate.json](certificate.json). Console output is in [logs/run-04.log](logs/run-04.log); the initial unwrapped run's fatal error is also retained in [logs/run-01.log](logs/run-01.log).

## Source materials

- [Paper DOI](https://doi.org/10.5194/agile-giss-4-13-2023)
- [Figshare article, version 1](https://figshare.com/articles/dataset/Does_spatial_thinking_ability_relate_to_performance_when_using_web-mapping_services_A_survey_with_digital_natives/22132940/1)

The original paper data and code remain linked at Figshare and were not uploaded with this certificate.
